from dataclasses import dataclass

@dataclass
class TestConfig:
    BASE_URL: str = 'https://useinsider.com/'
    CAREERS_URL: str = f'{BASE_URL}careers/quality-assurance/'
    TIMEOUT: int = 10
    BROWSER: str = 'chrome'
    HEADLESS: bool = False