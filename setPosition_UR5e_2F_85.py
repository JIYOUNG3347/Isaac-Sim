# Scripy Editor 동작용
from pxr import Usd, UsdGeom, UsdPhysics
import omni
import time
from omni.isaac.core import World
from omni.isaac.core.articulations import Articulation
from omni.isaac.core.utils.prims import is_prim_path_valid

# PhysicsScene 강제 생성
def ensure_physics_scene():
    stage = omni.usd.get_context().get_stage()
    path = "/physicsScene"
    if not stage.GetPrimAtPath(path).IsValid():
        UsdGeom.Xform.Define(stage, path)
        scene = UsdPhysics.Scene.Define(stage, path)
        scene.CreateGravityDirectionAttr().Set((0, 0, -1))
        scene.CreateGravityMagnitudeAttr().Set(9.81)
        print("[✅] PhysicsScene 생성 완료됨")
    else:
        print("[ℹ️] PhysicsScene 이미 존재함")

ensure_physics_scene()

# 시뮬레이션 월드
world = World(physics_dt=1/60.0, rendering_dt=1/60.0, stage_units_in_meters=1.0)
print("[✅] 시뮬레이션 월드 생성됨")

# 로봇 경로
robot_path = "/Root/UR5e"
if not is_prim_path_valid(robot_path):
    raise Exception(f"[❌] Prim '{robot_path}' 없음")
print(f"[✅] Prim 유효함: {robot_path}")

# 로봇 초기화
robot = Articulation(prim_path=robot_path, name="ur5e_robot")
robot.initialize()
print("[✅] 로봇 객체 생성 및 초기화됨")

# 관절 이름 확인
joint_names = robot.dof_names
print("[ℹ️] 관절 이름 목록:", joint_names)

# 💡 전체 14개 관절에 대한 위치 지정
#  - 앞 6개는 UR5e 로봇팔 관절
#  - 뒤 8개는 그리퍼를 열기 위한 값 (보통 0으로 설정하면 열림)
joint_positions = [
    0.0, -0.5, 0.5, -1.0, 1.2, 0.3,  # UR5e arm
    0.0, 0.0, 0.0, 0.0,              # Gripper joints (open)
    0.0, 0.0, 0.0, 0.0
]

robot.set_joint_positions(joint_positions)
print("[✅] 전체 관절 위치 설정 완료됨")
