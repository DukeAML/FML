from algorithms.asset_allocation import AssetAllocation

class AssetStrategy:

    def __init__(self, asset_allocation):
        super().__init__()
        self.asset_allocation = asset_allocation

    def allocate(self, date, positions, predictions):
        return self.asset_allocation.calculate_allocations( date, positions, predictions)