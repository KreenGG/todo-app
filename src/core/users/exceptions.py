from fastapi import HTTPException, status

UserNotFoundException = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

UserAlreadyExistsException = HTTPException(
    status.HTTP_409_CONFLICT,
    detail="User already exists",
)

InvalidCredentialsException = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
)
