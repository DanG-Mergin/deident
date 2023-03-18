from enum import Enum, IntEnum


class DocType(str, Enum):
    discharge_notes = "discharge_notes"
    discharge_summary = "discharge_notes"
    progress_notes = "progress_notes"
    progress_note = "progress_notes"


class PatientClass(str, Enum):
    inpatient = "inpatient"
    outpatient = "outpatient"
    emergency = "emergency"
    newborn = "newborn"
    maternity = "maternity"
    other = "other"
    preadmision = "preadmision"
