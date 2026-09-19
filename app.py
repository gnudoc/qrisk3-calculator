import streamlit as st
from cvd_risk import QRISK3, PatientData

st.set_page_config(page_title="QRISK3 Calculator", layout="wide")
st.title("QRISK3 Cardiovascular Risk Calculator")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Demographics & Vitals")
    age = st.number_input("Age", min_value=25, max_value=84, value=55)
    sex = st.selectbox("Sex", ["male", "female"])
    height = st.number_input("Height (cm)", value=175.0)
    weight = st.number_input("Weight (kg)", value=75.0)
    sbp = st.number_input("Systolic BP", min_value=70, max_value=210, value=120)
    # TODO: implement option to just give the last n SBP readings and calculate the sbps5
    sbps5 = st.number_input("Systolic BP Std Deviation (sbps5)", min_value=0.0, max_value=50.0, value=0.0)
    total_chol = st.number_input("Total Cholesterol (mmol/L)", min_value=2.0,max_value=12.0, value=5.0)
    hdl_chol = st.number_input("HDL Cholesterol (mmol/L)", min_value=0.5, max_value=5.0, value=1.2)
    # TODO: can we access an API or grab and parse a database to convert postcodes to depriv scores?
    townsend = st.number_input("Townsend Deprivation Score", min_value=-10.0, max_value=15.0, value=0.0)

with col2:
    st.header("Clinical History")
    smoking_options = {
        "Non-smoker": None,
        "Ex-smoker": 1,
        "Light smoker(<10/day)": 2,
        "Moderate smoker (10-19/day)": 3,
        "Heavy smoker (20+/day)": 4
    }
    smoke_choice = st.selectbox("Smoking Status", list(smoking_options.keys()))
    smoking_cat = smoking_options[smoke_choice]
    is_current_smoker = smoking_cat in [2, 3, 4]

    diabetes_choice = st.selectbox("Diabetes", ["None", "Type 1", "Type 2"])
    t1dm = (diabetes_choice == "Type 1")
    t2dm = (diabetes_choice == "Type 2")

    fhx_cvd = st.checkbox("Family History of CVD (1st degree <60y)")
    a_fib = st.checkbox("Atrial Fibrillation")
    ckd = st.checkbox("Chronic Kidney Disease (Stage 3-5)")
    bp_rx = st.checkbox("On Blood Pressure Treatment")
    migraine = st.checkbox("Migraine")
    ra = st.checkbox("Rheumatoid Arthritis")

with col3:
    st.header("QRISK3 Specifics")
    sle = st.checkbox("SLE")
    smi = st.checkbox("Severe Mental Illness (e.g. Schizophrenia)")
    antipsychotics = st.checkbox("On atypical antipsychotics")
    steroids = st.checkbox("On Regular Corticosteroids")
    ed = st.checkbox("Erectile Dysfunction / Impotence") if sex == "male" else False

if st.button("Calculate 10-Year Risk",type="primary"):
    try:
        bmi = weight / ((height/100.0) ** 2)
        patient_kwargs = dict(
            age=age,
            sex=sex,
            height_cm=height,
            weight_kg=weight,
            bmi=bmi,
            systolic_bp=sbp,
            total_cholesterol=total_chol,
            hdl_cholesterol=hdl_chol,
            smoking=is_current_smoker,
            family_history=fhx_cvd,
            atrial_fibrillation=a_fib,
            migraine=migraine,
            rheumatoid_arthritis=ra,
            renal_disease=ckd,
            type1_diabetes=t1dm,
            type2_diabetes=t2dm,
            treated_hypertension=bp_rx,
            townsend_deprivation=townsend,
            sbps5=sbps5,
            systemic_lupus=sle,
            severe_mental_illness=smi,
            atypical_antipsychotics=antipsychotics,
            corticosteroids=steroids,
            impotence2=ed
        )
        if smoking_cat is not None:
            patient_kwargs["smoking_category"] = smoking_cat
        patient = PatientData(**patient_kwargs)

        model = QRISK3()
        result = model.calculate(patient)

        st.success(f"**10-Year CVD Risk Score:** {result.risk_score:.1f}%")
        st.info(f"**Risk Category:** {result.risk_category.title()}")

    except Exception as e:
        st.error(f"Error calculating risk: {str(e)}")
