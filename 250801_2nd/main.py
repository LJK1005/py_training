class Team:
  def __init__(self, name: str, size: int) -> None: # 생성자
    self.name: str = name
    self.size: int = size

class QMC:
  def __init__(self, maas_flow: Team, gear_works: Team) -> None: # 생성자
    self.maas_flow: Team = maas_flow
    self.gear_works: Team = gear_works

  def introduce(self) -> None:
    print(f"MaaSFlow : {self.maas_flow.name}, {self.maas_flow.size}")
    print(f"GearWorks : {self.gear_works.name}, {self.gear_works.size}")

def main(args=None) -> None:
  maas_flow: Team = Team(name="마스플로우", size=2) # Team Class의 생성자 호출
  gear_works: Team = Team(name="기어웍스", size=2) # Team Class의 생성자 호출
  
  qmc: QMC = QMC(maas_flow=maas_flow, gear_works=gear_works)  # QMC Class의 생성자 호출
  qmc.introduce()

  # MaasFlow : 마스플로우, 2
  # GearWorks : 기어웍스, 2

if __name__ == "__main__":
  main()