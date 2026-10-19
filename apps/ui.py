from apps.service_session import ServiceSession


def main():
    print("meridian ui")
    session = ServiceSession()
    session.check_idle()
