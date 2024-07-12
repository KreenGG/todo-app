from fastapi import HTTPException, status

TodoNotFoundException = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="Todo not found",
)

BadRequestException = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="Bad request",
)
