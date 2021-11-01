import pandas as pd
import numpy as np
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()
inputCsv = args.file


# Read a csv
df = pd.read_csv(inputCsv, encoding="utf-16-be", encoding_errors="ignore",index_col=False)

# Drop columns that we don't need: Reason_other just says "Other", SubmittedDate is redundant
# formid and consent_check are the same for every form, extras are exactly what they sound like, and the attachment ones are redundant
df = df.drop(axis=1, columns=["reason_other", "SubmittedDate", "formid", "consent_check", "extra4", "extra5", "extra6", "extra7", "extra8", "extra9", "extra10", "Attachments", "record1AttachmentFileName", "record1AttachmentContentLength", "record2AttachmentFileName", "record2AttachmentContentLength", "inquiryForwardedTo", "dateInquiryCompleted"])

# Replace the reasons with something a little more palatable for the sheet
df.loc[df['reason_missingInfo'].notnull(), 'reason_missingInfo'] = "Missing Info"
df.loc[df['reason_outOfProvinceVaccine'].notnull(), 'reason_outOfProvinceVaccine'] = "Out of Province"
df.loc[df['reason_requestCopy'].notnull(), 'reason_requestCopy'] = "Print Record"
df.loc[df['reason_pharmacyVaccine'].notnull(), 'reason_pharmacyVaccine'] = "Doc/Pharm"

# Replace the weird attachment data with a "Yes" if it has an attachment, nan (null) if it doesn't
df['record1AttachmentContentType'] = df['record1AttachmentContentType'].replace({"image/jpeg": "Yes", "text/plain": np.nan})
df['record2AttachmentContentType'] = df['record2AttachmentContentType'].replace({"image/jpeg": "Yes", "text/plain": np.nan})
df = df.rename(columns={"record1AttachmentContentType": "Dose 1 Attachment", "record2AttachmentContentType": "Dose 2 Attachment"})

# Change dateInquirySent to proper date format
df['dateInquirySent'] = pd.to_datetime(df['dateInquirySent'], yearfirst=True)

# Add new blank columns for things like notes, assignee, and status
df = df.reindex(columns = df.columns.tolist() + ['Assigned to', 'Assigned Date', 'Dose1 Entered', 'Notes', 'Status Change Date', 'Validation Req\'d', 'Status', 'Assigned date', 'Duplicated', 'Region'])
df = df.reindex(columns = ["ConfirmationId", "dateInquirySent", "Assigned to", "Assigned Date", "Status", "Validation Req'd", "Status Change Date", "Notes", "covidOrSchool", "Dose1 Entered", "reason_missingInfo", "reason_outOfProvinceVaccine", "reason_requestCopy", "reason_pharmacyVaccine", "reasonForRequestOtherText", "name", "birthDate", "phin", "doNotHavePHIN", "phone", "email", "address", "city", "province", "postalCode", "RHA1", "locationDose1", "doNotRecallLoc1", "dateDose1", "doNotRecallDate1", "RHA2", "locationDose2", "doNotRecallLoc2", "dateDose2", "doNotRecallDate2", "schoolRequestDetails", "otherVaccines", "RHAOther", "locationDoseOther", "doNotRecallLocOther", "dateDoseOther", "doNotRecallDateOther", "Language", "Duplicated", "Region", "Dose 1 Attachment", "Dose 2 Attachment"])

# Finally, sort by ConfirmationId
df = df.sort_values(by=['ConfirmationId'])

# Save the cleaned file
df.to_csv('onetwo.csv', index=False)