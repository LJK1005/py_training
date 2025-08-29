import pandas as pd
import json
import os
import argparse

# ----------------------------------------------------------------
# 경로 설정: 현재 폴더 기준
# ----------------------------------------------------------------
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
BASE_DIR  : str   = os.path.dirname(SCRIPT_DIR)
INPUT_DIR : str  = os.path.join(BASE_DIR, "input")
OUTPUT_DIR: str = os.path.join(BASE_DIR, "output")

os.makedirs(INPUT_DIR,  exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_excel_to_json(
    excel_path: str,
    sheet_name: str,
    output_json: str = "gcv_wage_standard_work_time.json"
):
    """
    - 엑셀 A~P열(GroupID 포함 + 표준 작업시간) 읽어와 JSON 변환
    - header=3: 엑셀 4행(1-based)에서 L~P 컬럼명, A열은 GroupID
    - usecols="A:P": A열(GroupID), B~K빈열, L~P 작업정보
    - 빈 GroupID forward-fill 처리
    - 작업코드 없는 행 삭제
    - 한글 컬럼명을 snake_case 영문 키로 매핑
    - JSON 저장 시 ensure_ascii=False, indent=2
    """

    # 1) 엑셀 읽기
    df = pd.read_excel(
        excel_path,
        sheet_name=sheet_name,
        header=3,
        usecols="A:P",
        engine="openpyxl"
    )

    # 2) 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 3) 첫 열을 GroupID로
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "GroupID"})

    # 4) GroupID forward-fill
    df["GroupID"] = df["GroupID"].replace(["", "nan"], pd.NA).ffill()

    # 5) 필수 컬럼 확인
    required = ["작업코드", "작업명(중)", "작업명(한)", "M/H", "비고"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"필수 컬럼이 없습니다: {missing}. 실제 컬럼명: {df.columns.tolist()}")

    # 6) 작업코드 없는 행 제거
    df = df.dropna(subset=["작업코드"], how="all")

    # 7) 문자열 컬럼 전처리
    text_cols = ["GroupID", "작업코드", "작업명(중)", "작업명(한)", "비고"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().replace({"nan": None, "": None})

    # 8) M/H 숫자형 변환
    df["M/H"] = pd.to_numeric(df["M/H"], errors="coerce").fillna(0.0)

    # 9) 비고 null 처리
    mask = df["비고"].isin(["/", None])
    df.loc[mask, "비고"] = None

    # 10) 한글→영문 컬럼 매핑
    column_mapping = {
        "GroupID":      "group_id",
        "작업코드":       "work_code",
        "작업명(중)":     "work_name_cn",
        "작업명(한)":     "work_name_ko",
        "M/H":          "man_hours",
        "비고":          "remarks",
    }
    df = df.rename(columns=column_mapping)

    # 11) 출력 컬럼 순서 지정
    ordered = list(column_mapping.values())
    df = df[[c for c in ordered if c in df.columns]]

    # 12) JSON 저장
    records = df.to_dict(orient="records")
    with open(output_json, "w", encoding="utf-8") as fp:
        json.dump(records, fp, ensure_ascii=False, indent=2)

    print(f"✅ '{output_json}' 파일 저장 완료! 총 {len(records)}개 레코드")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GCV 보증 공임 엑셀 → JSON 변환기")
    parser.add_argument("-e", "--excel", required=True, help="엑셀 파일 경로")
    parser.add_argument("-s", "--sheet", required=True, help="시트명")
    parser.add_argument("-o", "--output", required=True, help="출력 JSON 파일 경로")

    args = parser.parse_args()

    convert_excel_to_json(
        excel_path=args.excel,
        sheet_name=args.sheet,
        output_json=args.output
    )
