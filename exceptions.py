class GetHtmlError(Exception):
    def __init__(self, message: str = "Something went wrong while requesting HTML", status_code: int = 0, reason: str = "No fucking reason"):
        self.message = message + f"Status: {status_code} | {reason}"
        super().__init__(self.message)
