if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from enum import Enum


class GoogleAPI(Enum):
    COCOBLANC_RPA_SHEET_KEY = {
        "type": "service_account",
        "project_id": "sabangnet-384800",
        "private_key_id": "bea2b7498803b5350e238b99385922184d004a3a",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQD5I4YIe2YFwHxL\ndA7axe5AhTixsJmmhNS53nYrFCPavAfVlUMwNbLE3Xzh+36azn68wJIjtsfhOOhE\nteRqyIPA6G+vS6VDglCeyXte4BVLTbExgEvn6XFxrqnkGLlamy5ilkcRSIf8qWpD\nuqk+9FkvDKUpT4L4LKn7ym3/Q+0+eXjNkkYdZ74/R7AvbIENNS41FmnAtjnCSWg9\naxm7uUenQUGY0WSa8MfkJ6mpfh2y1FRxifTTZ/Dzr/xyRDICD6f0M4iVMbxjCnMY\nKv4gG+Y/p6zV1f53Kutkng0NAECK3fIgFCRVJ3zzuHrxfu/dMc4kTnSglU9iV6gf\ndTbOLEqBAgMBAAECggEAd8BAc6FEp60e0XHGlhefbnnah2ZYZHbifTjV2d0DYucQ\naPQm6GxXMlM37LNi5mws9PMnC22W48XjtusrELyyv625ySt2E132/GviFfdlpN2C\nN0Xwtlc6BSesV4wew9NlV1PecwtG+gZAoq99HFp856WPWazzSfDF/9YMSy9OQMFV\nqJberN4Vaqqe7AYPMnZFs2zp01rsgEVtmvJfOaXrvqhuHyJKHXjnGdR7JJ4T+6xl\ngOF3DSNRPbpzHX4zs1GB4skCbs5PQyGmm+BuO3xXJCRGj38txtTcXPO95Jj/UBcm\nFD/lV0E0tuRO09gdSa7hfeqha7gZAZdIpoh2/KKOdQKBgQD/bRP6NEnkHDEiCdnY\nM7ayB608lPdrnESe3Df5W7XN75Sk3X5CPjHpCEeXrBRt20z5Ejf+Quo/fAbSUaYw\nZ5pCi3Vm7XUslSFs5PGLvDC58yOxcqp6meEVCfG9zAwuvbl85jXQOLjDKos9dsp3\ncHRNKGUjtyjAAo4jnviPSiCXNwKBgQD5stQ8CHrHZhvhsUFVaIM0k0QoPFu/8QAh\niyJBBRtZPQY4JIWZY2SihSZ21WlKuzAQ+mDcJ+F6bLudDliDV6F9dj32jXTyzwQl\nLMV+ayWTIWycp+6tG4J0Y1XXrKASikezv/Wr/gSTHjsZN3TvQWH+2CL0yM6rCkJY\nAnLXVz0YBwKBgDcgE2+sWUYhz3jJJ3rBrmw9u+WXQM64qxad8HaglFwdmLb8FoO1\naJAieVECkmYjLjmS9QKq7mNFITPC61sHAQPblTrhhKhahxw5TOgbdWisUMe7N4++\nJhWkT8fmgbqUt7N8+6A0nauBQwvA13Fvk6oTTcCnhuPpqUOGy54hIWeBAoGAXyEK\nSnTQkfcM2Ec3pNpUYktYxBt6uP2QFzdyrWLMsIrXO7xuSancRS6FIPDdVGNMRKuf\nC0EGXiXetE8q2Z8hHzNVGAF8dKT550/PTgJ0JkGtp2EzRTAd20mdArX5phaYipqv\ndf8orwPtcAX4vs4iD304lBmM4wzdibolFnVeCTECgYB/bfExyAU/y0HmQGVh2RA9\n1VSPAuzWIKaXZZadRxyGqbar6yO2nK7WFYhfrzPg9Hdp6geXK8l/R2F8KaW/qqUO\nQrKDRRwMbehxSPzSPFbC1ooHCAmzeIXMwVP2hUvSDvdjexcr66kBBIX8WWD7TM/l\ncQFA0CKD42BHzDaBN6h+YA==\n-----END PRIVATE KEY-----\n",
        "client_email": "sabangnet-gspread@sabangnet-384800.iam.gserviceaccount.com",
        "client_id": "116767938427302750423",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "revoke_uri": "https://oauth2.googleapis.com/revoke",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sabangnet-gspread%40sabangnet-384800.iam.gserviceaccount.com",
        "scopes": [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ],
    }


class GoogleSheets(Enum):
    PRODUCT_SETTING_URL = "https://docs.google.com/spreadsheets/d/1AoxHlFbAW_FS7oUxwSUUX81oiwsGzY7o4iwstBAqMgs"


if __name__ == "__main__":
    pass
