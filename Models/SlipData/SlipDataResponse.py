from typing import Any
from dataclasses import dataclass
import json
@dataclass
class slip_data_response:
    fromacc : str
    frombank : str
    fromaccno : str
    to: str
    tobank: str
    toaccno: str
    transactionno: str
    amount: str

    @staticmethod
    def from_dict(obj: Any) -> 'slip_data_response':
        _from = str(obj.get("from"))
        _frombank  = str(obj.get("frombank"))
        _fromaccno  = str(obj.get("fromaccno"))
        _to = str(obj.get("to :"))
        _tobank = str(obj.get("tobank"))
        _toaccno = str(obj.get("toaccno"))
        _transactionno = str(obj.get("transactionno"))
        _amount = str(obj.get("amount"))
        return slip_data_response(_from, _frombank , _fromaccno , _to, _tobank, _toaccno, _transactionno, _amount)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)