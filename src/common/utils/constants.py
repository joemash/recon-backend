CONTENT_TYPES = (
    ("image/png", "PNG"),
    ("image/jpeg", "JPEG"),
    ("application/pdf", "PDF"),
    ("application/vnd.ms-excel", "xlsx"),
    ("application/msword", "doc"),
    (
        "application/vnd.openxmlformats-officedocument.wordprocessingml." "document",
        "docx",
    ),
    (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "xlsx",
    ),
)

EMAIL = "email"
PHONE_NUMBER = "phone_number"
CONTACT_TYPES = [[EMAIL, "E-mail Address"], [PHONE_NUMBER, "Phone Number"]]
