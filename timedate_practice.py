from datetime import datetime,timezone


def get_activity_status(pushed_at):
    push_date = datetime.strptime(
        pushed_at,
        "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)
    current_time = datetime.now(timezone.utc)
    difference = current_time - push_date
    if difference.days<= 180:
        return "Active"
    return "Stale" 


def main():
    date_text = "2024-08-20T23:54:42Z"
    print(get_activity_status(date_text))


if __name__ == "__main__":
    main()

