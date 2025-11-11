
import grpc
import os

import grpc_generated.admin_pb2 as admin_pb2
import grpc_generated.admin_pb2_grpc as admin_pb2_grpc

GRPC_SERVER_URL = os.environ.get("GRPC_SERVER_URL", "grpc_server:50051")

async def close_poll_via_grpc(poll_id: int) -> str:
   
    async with grpc.aio.insecure_channel(GRPC_SERVER_URL) as channel:
        stub = admin_pb2_grpc.AdminServiceStub(channel)

        request = admin_pb2.ClosePollRequest(poll_id=poll_id)

        response = await stub.ClosePoll(request)

        return response.status