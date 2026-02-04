from __future__ import annotations

import json
from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..deps import get_current_user
from ..models import ManualRequest, ManualResponse, User
from ..schemas import ManualAnalysisRequest, ManualAnalysisResponse
from ..services.llm import llm_client

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/manual", response_model=ManualAnalysisResponse)
def manual_analysis(
    data: ManualAnalysisRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    titles = [title.strip() for title in data.titles if title.strip()]
    request = ManualRequest(user_id=user.id, titles_json=json.dumps(titles, ensure_ascii=False))
    session.add(request)
    session.commit()
    session.refresh(request)

    response_text = llm_client.analyze_titles(titles)
    response = ManualResponse(request_id=request.id, model=llm_client.model, response_text=response_text)
    session.add(response)
    session.commit()
    session.refresh(response)

    return ManualAnalysisResponse(
        request_id=request.id,
        model=response.model,
        response_text=response.response_text,
        created_at=response.created_at,
    )
