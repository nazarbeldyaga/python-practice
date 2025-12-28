from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any


class PingPayload(BaseModel):
    message: str

class QNTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")

    hash: str
    blockNumber: str
    blockHash: str
    from_address: str = Field(..., alias="from")
    to: Optional[str] = None
    value: str
    input: str
    nonce: str
    transactionIndex: str
    type: str

    gas: Optional[str] = None
    gasPrice: Optional[str] = None
    chainId: Optional[str] = None
    v: Optional[str] = None
    r: Optional[str] = None
    s: Optional[str] = None

    maxFeePerGas: Optional[str] = None
    maxPriorityFeePerGas: Optional[str] = None
    maxFeePerBlobGas: Optional[str] = None
    blobVersionedHashes: Optional[List[str]] = None
    yParity: Optional[str] = None
    accessList: Optional[List[Any]] = None

class QNMetadata(BaseModel):
    stream_id: str
    stream_name: str
    network: str
    dataset: str
    batch_start_range: int
    batch_end_range: int
    data_size_bytes: int

class QNPayload(BaseModel):
    data: List[List[QNTransaction]]
    metadata: QNMetadata