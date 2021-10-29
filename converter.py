import pandas as pd
import numpy as np

df = pd.read_csv("1634980-1635017_Oct-27-2021--16-16_combined.csv", encoding="utf-16-be", encoding_errors="ignore",index_col=False)
# Drop columns that we don't need: Reason_other just says "Other", SubmittedDate is redundant
# formid and consent_check are the same for every form, extras are exactly what they sound like, and the attachment ones are redundant
df = df.drop(axis=1, columns=["reason_other", "SubmittedDate", "formid", "consent_check", "extra4", "extra5", "extra6", "extra7", "extra8", "extra9", "extra10", "Attachments", "record1AttachmentFileName", "record1AttachmentContentLength", "record2AttachmentFileName", "record2AttachmentContentLength", "inquiryForwardedTo", "dateInquiryCompleted"])
# Replace the reasons with something a little more palatable for the sheet
df.loc[df['reason_missingInfo'].notnull(), 'reason_missingInfo'] = "Missing Info"
df.loc[df['reason_outOfProvinceVaccine'].notnull(), 'reason_outOfProvinceVaccine'] = "Out of Province"
df.loc[df['reason_requestCopy'].notnull(), 'reason_requestCopy'] = "Print Record"
df.loc[df['reason_pharmacyVaccine'].notnull(), 'reason_pharmacyVaccine'] = "Doc/Pharm"
df = df['record1AttachmentContentType'].replace({"image/jpeg": "Yes", "text/plain": np.nan})
# Add new blank columns for things like notes, assignee, and status
#df = df.reindex(columns = df.columns.tolist() + ['Assigned to', 'Dose1 Entered', 'Notes', 'Status Change Date', 'Validation Req\'d', 'Status', 'Assigned date', 'Duplicated', 'Region'])
df.to_csv('onetwo.csv', index=False)