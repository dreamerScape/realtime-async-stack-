import grpc
import logging
import asyncio
from concurrent import futures

import grpc_generated.admin_pb2 as admin_pb2
import grpc_generated.admin_pb2_grpc as admin_pb2_grpc

from db.session import SyncSessionLocal
from models.poll import Poll

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class AdminServiceImpl(admin_pb2_grpc.AdminServiceServicer):

    def ClosePoll(self, request, context):
        poll_id = request.poll_id
        log.info(f"gRPC: Received request to close poll {poll_id}")

        try:
            with SyncSessionLocal() as db:
                poll_to_close = db.query(Poll).filter(Poll.id == poll_id).first()

                if not poll_to_close:
                    log.warning(f"gRPC: Poll {poll_id} not found.")
                    return admin_pb2.ClosePollResponse(status="Poll not found")

                # 2. Обновляем
                poll_to_close.question = f"[CLOSED] {poll_to_close.question}"
                db.commit()

            log.info(f"gRPC: Poll {poll_id} closed.")
            return admin_pb2.ClosePollResponse(status="Poll closed successfully")

        except Exception as e:
            log.error(f"gRPC: Error closing poll: {e}")
            return admin_pb2.ClosePollResponse(status=f"Error: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_pb2_grpc.add_AdminServiceServicer_to_server(
        AdminServiceImpl(), server
    )
    server.add_insecure_port('[::]:50051')
    log.info("Starting gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()