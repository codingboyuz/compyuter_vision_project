# from onvif import ONVIFCamera
# import cv2
#
# def get_rtsp_url(ip, port, username, password):
#     camera = ONVIFCamera(ip, port, username, password)
#
#
#     resp = camera.devicemgmt.GetHostname()
#     print(f"resp:{resp}")
#
#     # Create ptz service
#     ptz_service = camera.create_ptz_service()
#     # Get ptz configuration
#     print(
#     ptz_service.user
#
#     )
#     # Another way
#     ptz_service.GetConfiguration()
#
#
#     media_service = camera.create_media_service()
#     profiles = media_service.GetProfiles()
#     profile = profiles[0]
#     print(f"profile:{profile}")
#
#     stream_setup = media_service.create_type('GetStreamUri')
#     stream_setup.StreamSetup = {
#         'Stream': 'RTP-Unicast',
#         'Transport': {'Protocol': 'RTSP'}
#     }
#     stream_setup.ProfileToken = profile.token
#
#     uri_response = media_service.GetStreamUri(stream_setup)
#
#     return uri_response.Uri
#
#
#
# def show_camera(rtsp_url:str):
#     cap = cv2.VideoCapture(rtsp_url)
#
#     if not cap.isOpened():
#         print("❌ Kameraga ulanib bo‘lmadi.")
#         return
#     #
#     # # 🎯 O'lchamni belgilash: width=1920, height=1080
#     # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#     # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#
#     print("✅ Kamera ochildi. 'q' tugmasi bilan chiqiladi.")
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("⚠️ Kadr olinmadi.")
#             break
#
#         frame = cv2.resize(frame, (1920, 1080))
#         cv2.imshow("IP Kamera", frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#
#
# if __name__ == "__main__":
#     # ONVIF kamera ma'lumotlari
#     ip = '192.168.1.136'
#     port = 80
#     username = 'admin'
#     password = '123456'
#
#     try:
#         rtsp_url = get_rtsp_url(ip, port, username, password)
#         print(f"🎥 RTSP URL: {rtsp_url}")
#         show_camera(rtsp_url)
#     except Exception as e:
#         print(f"❌ Xatolik: {e}")
# -*- coding: utf-8 -*-
#
#
#
