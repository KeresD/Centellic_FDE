import llm
from anthropic import APIStatusError, APITimeoutError, RateLimitError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from routers.firms import get_firm_or_404

router = APIRouter(prefix="/firms", tags=["insights"])

# create a post endpoint for /firms/{firm_id}/summary
# it should take in a firm and find it (or not...)
# try to make the llm call to get a summary of the call
    # if unsuccessfull raise an appropriate Error and status code


@router.post("/{firm_id}/summary")
def get_firm_summary(firm: dict = Depends(get_firm_or_404)):
    try:
        return llm.summarise_firm(firm)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Summary provider timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Summary provider's rate limit exceeded")
    except APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"Summary provider has an API error: {e}")
    # except Exception as e:
        # jst suggests a generic bug and a good catch all for 500 errors
        # dnt choose to return - it gets returned as default by FastAPI
        # authentication error would bring a error 500
        # would use a 500 error when there aren't enough 500 errors implemented in the code
        # raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/{firm_id}/summary/estimate")
def estimate(firm: dict = Depends(get_firm_or_404)):
    try:
        return {
            "id": firm["id"],
            "est_input_tokens": llm.est_input_tokens(firm),
            "model": llm.MODEL,
        }
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Token count request timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Token count provider's rate limit exceeded")
    except APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"Token count provider API error: {e}")
    
@router.get("/{firm_id}/summary/stream")
def stream_summary(firm: dict = Depends(get_firm_or_404)):
    return StreamingResponse(
        llm.stream_firm_summary(firm),
        media_type="text/plain",
    )
    
# endpoint challenge
# POST endpoint at firms/firm_id/analysis
# tries to analyse firm, if not, raises appropriate exception(s)
@router.post("/{firm_id}/analysis")
def analyse_firm_endpoint(firm: dict = Depends(get_firm_or_404)):
    try:
        return llm.analyse_firm(firm)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Analysis provider timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Analysis provider's rate limit exceeded")
    except APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"Analysis provider has an API error: {e}")
# check: curl -X POST http://127.0.0.1:8000/firms/1/analysis
# output: {"id":1,"name":"Harding & Voss","analysis":{"tier":"national","strengths":["Substantial revenue base of 
# £1,240m demonstrating significant market presence","Large lawyer cohort of 1,850 professionals providing broad service capacity",
# "Established partnership structure with 210 equity partners"],"risks":["Revenue per lawyer of approximately £670k suggests potential 
# profitability pressures relative to elite competitors","Large headcount may indicate complexity in firm management and coordination",
# "Scale without magic circle positioning may limit premium client attraction"],"headcount_efficiency":"medium"},"input_tokens":479,
# "output_tokens":117,"stop_reason":"end_turn"}

