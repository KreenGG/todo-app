from fastapi import HTTPException, status

TodoNotFoundException = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="Todo not found",
)
