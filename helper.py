from functools import wraps


def admin_filter(admins_id: list[int]):
    def decorator(func):
        @wraps(func)
        async def wrapper(msg, *args, **kwargs):
            if msg.from_user.id in admins_id:
                return await func(msg, *args, **kwargs)
            return

        return wrapper

    return decorator
