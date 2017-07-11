class MathUtils:
    @staticmethod
    def remap(value: int, from_low: int, from_high: int, to_low: int, to_high: int) -> int:
        return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)