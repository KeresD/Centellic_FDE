# Challenge: review the contractor's code

**30 minutes. In pairs. Talk the whole way through.**

---

## The scenario

A contractor built a `reports` resource for the Firm Intelligence API and left the
engagement. It works — every endpoint returns something, nothing crashes, and it passed
whatever review it got, which was none.

You are the pair picking it up. Your client is about to put it in front of real users, and
they've asked one question: **is this safe to ship?**

Drop `reports.py` into your `routers/` folder and wire it up in `main.py` alongside the other
two:

```python
from routers import firms, people, reports

app.include_router(reports.router)
```

Run it. Confirm `GET /reports` returns two reports. Now review it.

---

## How to run the 30 minutes

**Minutes 0–5 — read alone. No talking.**
Both of you read the whole file in silence and write your own list of anything that concerns
you. Do not compare yet. This matters: if one of you talks first, the other stops looking and
starts agreeing.

- doesn't have a health check so can't can't issues and relies on other error status' --> 5
- time sleep in async def --> 4 causes serious delays in pr -> if server was big it would be 1
- validation to make sure firm_id actually exists but one for report_id exists
- view_counts not deleted when report is deleted --> 1
  - GET view_counts - if same user runs same pr twice then view count = +1
- POST create_report() - if client made multiple pr then there can be duplicate records - needs an idempotency key --> 2
- PUT update_report - every time a client makes a pr the records are not checked to see if changes are needed. Records are jst changed and changes revisions. --> 3

**Minutes 5–15 — compare, argue, rank.**
Now compare lists. For each thing either of you flagged:
- Is it actually a problem, or just unfamiliar?
- What would a caller *see* when it goes wrong?
- Is it a problem today, or only under load / on a flaky network?

Then do the part that matters most: **rank them, worst first.** You must agree an order.
"Worst" is your call — argue for what you mean by it. Blast radius? Data integrity? How likely
it is to actually happen? There's no answer key for the ranking.

**Minutes 15–25 — fix your number one.**
Only the top one. Make the change, run the server, and prove it's fixed with a `curl` that
would have demonstrated the bug before. If you finish early, go to number two.

**Minutes 25–30 — prepare a 60-second handover.**
You're briefing the client's engineering lead. Prepare, out loud between you:
- The ranked list, and one sentence on why your number one is number one
- What you fixed, and the command that proves it
- What you did *not* fix, and what you'd need to do it properly

---

## Constraints

- **Do not rewrite the file.** This is a review, not a rebuild. Minimal diffs only.
- **Every claim needs a command.** If you say an endpoint is broken, be able to show it
  breaking. "It looks wrong" is not a finding.
- **Assume the contract is already public.** Other teams call these endpoints. You may not
  rename a path, a field, or change a status code without saying out loud that it's a breaking
  change and why it's worth it.

---

## Hints, if you're stuck at minute 8

Not a checklist — five questions worth asking of any endpoint:

1. If a client sent this request **twice**, what would be different the second time?
2. If the network dropped the response, would a retry be **safe**?
3. Does this endpoint change state that its HTTP method doesn't imply it changes?
4. Is anything in here going to make **other, unrelated** requests slow?
5. Why does this file look different from `firms.py`, and does the difference matter?

---

## What good looks like

A pair that finishes strong can say something like:

> "There are four problems. The worst is X, because Y — here's a command that shows it. We
> fixed it by Z, and this command proves it. We'd also deal with W, but it's a breaking change
> so it needs a conversation first. The one we deliberately left alone is V, because we don't
> think it's actually wrong, and here's our reasoning."

That's the handover. Not a list of complaints — a ranked judgement, with evidence, and an
honest line between what you fixed and what you'd need permission for.

## In order of priority:

### Issue 1:
- time sleep in async def --> causes serious delays in pr

#### Check in terminal: 
  - curl http://127.0.0.1:8000/reports/1/export & sleep 0.2 && time curl http://127.0.0.1:8000/firms/health
[1] 19517
{"id":1,"title":"UK Market Outlook","format":"pdf"}{"status":"ok"}[1]  + done       curl http://127.0.0.1:8000/reports/1/export
curl http://127.0.0.1:8000/firms/health  0.01s user 0.01s system 0% cpu 2.811 total
#### FIX: 
  `import asyncio` and implement into code

  `report = get_report_or_404(report_id)
    await asyncio.sleep(3)
    return {"id": report["id"], "title": report["title"], "format": "pdf"}`


### Issue 2:
- view_counts not deleted when report is deleted

#### Check:
- curl http://127.0.0.1:8000/reports/2                  # bump view count on report 2
  - {"id":2,"title":"US Partner Compensation","firm_id":2,"revisions":["v1"],"views":1}

- curl -X DELETE http://127.0.0.1:8000/reports/2         # delete the highest-id report

curl -X POST http://127.0.0.1:8000/reports \
  -H "Content-Type: application/json" \
  -d '{"title": "New Report", "firm_id": 1}'           # gets id=2 again (max+1 reuse)
  - {"id":2,"title":"New Report","firm_id":1,"revisions":["v1"]}

- curl http://127.0.0.1:8000/reports/2                   # views shows stale count from deleted report
  - {"id":2,"title":"New Report","firm_id":1,"revisions":["v1"],"views":2}

#### Fix:

- Before: @router.delete("/{report_id}", status_code=204)
def delete_report(report_id: int):
    report = get_report_or_404(report_id)
    REPORTS.remove(report)
    return

- Add this to the function: `_view_counts.pop(report_id, None)`
 ` @router.delete("/{report_id}", status_code=204)
  def delete_report(report_id: int):
      report = get_report_or_404(report_id)
      REPORTS.remove(report)
      _view_counts.pop(report_id, None)
      return
  `
### Issue 3:
- POST create_report() - if client made multiple pr then there can be duplicate records - needs an idempotency key

#### Check:
- curl -X POST http://127.0.0.1:8000/reports \
  -H "Content-Type: application/json" \
  -d '{"title": "Duplicate Test", "firm_id": 1}'
  - {"id":3,"title":"Duplicate Test","firm_id":1,"revisions":["v1"]}
- curl -X POST http://127.0.0.1:8000/reports \
  -H "Content-Type: application/json" \
  -d '{"title": "Duplicate Test", "firm_id": 1}'
  - {"id":4,"title":"Duplicate Test","firm_id":1,"revisions":["v1"]}
- curl http://127.0.0.1:8000/reports
  - [{"id":1,"title":"UK Market Outlook","firm_id":1,"revisions":["v1"]},{"id":2,"title":"New Report","firm_id":1,"revisions":["v1"]},{"id":3,"title":"Duplicate Test","firm_id":1,"revisions":["v1"]},{"id":4,"title":"Duplicate Test","firm_id":1,"revisions":["v1"]}]
  - output has 2 different "id" but everything else remains the same

  #### Fix:
  @router.post("", status_code=201)
def create_report(
    new: NewReport,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    if idempotency_key in _idempotency_keys:
        return _idempotency_keys[idempotency_key]

    new_id = max(report["id"] for report in REPORTS) + 1
    report = {
        "id": new_id,
        "title": new.title,
        "firm_id": new.firm_id,
        "revisions": ["v1"],
    }

    REPORTS.append(report)
    _idempotency_keys[idempotency_key] = report

    return report

### Issue 4:
- PUT update_report - every time a client makes a pr the records are not checked to see if changes are needed. Records are jst changed and changes revisions.

#### Check:
- curl -X PUT http://127.0.0.1:8000/reports/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "UK Market Outlook", "firm_id": 1}'
  - {"id":1,"title":"UK Market Outlook","firm_id":1,"revisions":["v1","v2"]}
- curl -X PUT http://127.0.0.1:8000/reports/1 \
  -H "Content-Type: application/json" \ 
  -d '{"title": "UK Market Outlook", "firm_id": 1}'
  - {"id":1,"title":"UK Market Outlook","firm_id":1,"revisions":["v1","v2","v3"]}
- curl http://127.0.0.1:8000/reports/1
  - {"id":1,"title":"UK Market Outlook","firm_id":1,"revisions":["v1","v2","v3"],"views":1}

#### Fix:
@router.put("/{report_id}")
def update_report(report_id: int, new: NewReport):
    report = get_report_or_404(report_id)
    changed = (report["title"] != new.title) or (report["firm_id"] != new.firm_id)
    report["title"] = new.title
    report["firm_id"] = new.firm_id
    if changed:
        report["revisions"].append(f"v{len(report['revisions']) + 1}")
    return report

### Issue 5:
- validation to make sure firm_id actually exists but one for report_id exists

#### Check:
- curl -X POST http://127.0.0.1:8000/reports \
    -H "Content-Type: application/json" \
    -d '{"title": "Ghost Firm Report", "firm_id": 9999}'
  - {"id":5,"title":"Ghost Firm Report","firm_id":9999,"revisions":["v1"]}
  - shows a firm that's not on record so clients may assume firm exists even though it's not on record.
  - needs a 404 error

#### Fix:
`from data import FIRMS`

`def validate_firm_id(firm_id: int):
    if not any(f["id"] == firm_id for f in FIRMS):
        raise HTTPException(status_code=422, detail=f"No firm with id {firm_id}")
`

### Missing Health Check
