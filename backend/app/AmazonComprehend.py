import boto3
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
from django.conf import settings

comprehend = boto3.client('comprehend')
FilePath_1 = settings.MEDIA_ROOT+"/uplodedFiles/"
# FilePath_1 = "/var/www/html/ocrApp/assets/temp/"
s3_client = boto3.client('s3', region_name='us-east-1')
bucket_name = 'ocrnlp'



@csrf_exempt
def amazonComprehend(req):



    job_id_string = req.POST.get('job_id_string')
    print("job id string in get textract results", job_id_string)
    id = req.POST.get('caseId')
    file = req.POST.get('file')
    path = req.POST.get('path')
    # text = req.POST.get('text')
    tempfilename = str(file).split(".")[0]
    tempfilename = tempfilename.replace(" ", "-")
    s3_client = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'ocrnlp'

    DetectSentimenttext = "WELCOME FUNDS INC.  OF WELCOME FUNDS IN  STRICTLY PROHIBITED  JOHN HANCOCK LIFE INSURANCE COMPANY (U.S.A.)  August 2 2019  Dear Policyowner:  RE: Policy No. 59 710 467  Insureds: PHILLIP BAUM  JOAN L BAUM  John Hancock Life Insurance Company (U.S.A.)  To assist you in the effective management of your universal life insurance policy  we have enclosed a package of updated information about your policys performance.  The information package includes:  1. Your policy annual statement which summarizes your policys activity during the  past year. You can use your annual statement to verify your current coverage  policy values payments and charges. There are several factors that will impact  the growth in your universal life policy namely:  The amount and frequency of your premium payments  Interest credited and its compounding effect over time  The long-term effects of the monthly deductions for cost of insurance expenses  and cost of any supplemental benefits. The deductions for cost of insurance  will increase over time as the insureds age.  2. A Snapshot illustration of your policy that provides a current \point in time\  view of your policys benefits and values employing certain static assumptions  relating to mortality and interest rates based on guaranteed and not guaranteed  values. We have created this Snapshot illustration using information we have on  file regarding your policy. Keep in mind that interest rates will fluctuate and  the effect on performance of these fluctuations will be compounded over time.  The interest rate credited to your guaranteed interest account has decreased since  your last anniversary. Please see your annual statement for details.  We recommend that you carefully review this information package with your insurance  representative and/or financial advisors. It is important to remember that the  primary advantage of universal life is its flexibility allowing you to adjust your  premium payment schedule death benefit option or face amount in response to  changing economic conditions or needs. If you would like more information on your  policy or want to see an illustration more tailored to your personal objectives  please contact your representative  Customer Service Center at  or our  Sincerely  Customer Service Center  Life Post Issue - Customer Service Center  John Hancock Life Insurance Company (U.S.A.)  PO Box 55979 Boston MA 02205  Toll Free: (800) 387-2747 Fax: (617) 572-1571  www.jhlifeinsurance.com \n Page Num   1 \n  Page Num   2 \n John Shousa  WELCOME FUNDS INC.  PROPORTY Hancock. OF WELCOME FUNDS INC. Your IINAUTHORIZED Policy Annual USE STRICTLY Statement PROHIBITED  4  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  Statement date - Aug 2 2019  SUMMARY OF POLICY - Survivorship Flexible Premium Adjustable Life  Policy Number  59 710 467  Lives Insured  Policy Date  Aug 2 2005  PHILLIP BAUM  Base Face Amount  $1691520.00  JOAN L BAUM  Supplementary Insurance Face Amount  Level Death Benefit  $0.00  Schedule Premium  $0.00  Gross Death Benefit  $1691620.00  Payable ANNUALLY  Less Loan  For information on your supplementary  Net Death Benefit  $1691620.00  benefits please see page 4  This statement covers the period from Aug 2 2018 to Aug 1 2019  POLICY VALUE  Opening Balance  $504811.97  as of Aug 2 2018  Total Premiums Received  $0.00  Premium Charge  $0.00  Cost Of Insurance  $8412.97-  Administrative Charge  $240.00-  Contract Charge  $1796.52-  Coverage Expense Charge  $1725.48-  Cost of Suppl. Benefits  $3434.64-  Premium Load Refund  $0.00  Interest  $20866.72  Partial Withdrawals  $0.00  Pro-Rata Surrender Charges  $0.00  Policy Benefits Credited  $0.00  Policy Value as of  $510069.08  Aug 1 2019  SURRENDER VALUE  Surrender Charge  as of Aug 1 2019  $4427.94-  Cash Surrender value  $505641.14  Less  Closing Loan Balance  Interest Accrued  Net Cash Surrender Value  $505641.14  as of Aug 1 2019  20850  Page 1 of 8  BBHG  www.jhlifeinsurance.com \n Page Num   2 \n  Page Num   3 \n WELCOME FUNDS INC.  FUNDS INC.  LJNAUTHORIZED USE STRICTLY PROHIBITED  Your Policy Annual Statement  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  POLICY NUMBER: 59 710 467  FOR YOUR INFORMATION  1. The following interest rates were credited to the guaranteed interest  account during the past year. The interest rate will never be below .00%.  Aug  2 2018 To Aug 31 2018  4.35  Sep 1 2018 To Sep 30 2018  4.35  Oct  1 2018  Oct 31  2018  4.35  Nov  1 2018  Nov 30  2018  4.35  Dec  1 2018  Dec 31  2018  4.35  Jan  1 2019  Jan 31  2019  4.35  Feb  1 2019  Feb  28  2019  4.35  Mar  1 2019  Mar  31  2019  4.00  Apr  1 2019  Apr  30  2019  4.00  May  1 2019  May 31  2019  4.00  Jun  1 2019  Jun  30  2019  4.00  Jul  1 2019  Jul 31 2019  4.00  Aug  1 2019  Aug 1 2019  4.00  The interest rate credited to your guaranteed interest account has decreased since  your last anniversary. Please see the above schedule for details.  2. Loan interest is charged at a rate of  6.00%  Page 2 of 8  www.jhlifeinsurance.com \n Page Num   3 \n  Page Num   4 \n WELCOME FUNDS INC.  COCKIELCOME FUNDS INC.  | LAALTHORIZED USE STRICTI Y PROHIBITED  Your Policy Annual Statement  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  Policy Number: 59 710 467  Projected monthly deductions for the coming year (assuming current rates  current charges and that the scheduled premium is paid) :  Cost of  Loadings  Cost of  Month  Insurance  and Expenses  Suppl. Benefits  1  $857.46  $313.50  $286.22  2  $857.31  $313.50  $286.22  3  $857.15  $313.50  $286.22  4  $857.00  $313.50  $286.22  5  $856.85  $313.50  $286.22  6  $856.69  $313.50  $286.22  7  $856.54  $313.50  $286.22  8  $856.39  $313.50  $286.22  9  $856.23  $313.50  $286.22  10  $856.07  $313.50  $286.22  11  $855.92  $313.50  $286.22  12  $855.76  $313.50  $286.22  Policy Protection Rider (Enhanced) Information (as of Aug 1 2019)  Your Policy was issued with the Policy Protection Rider (Enhanced)  for a benefit of 32 years and is scheduled to terminate  on Aug 2 2037. This benefit protects your policy from lapsing.  As long as the Policy Protection Rider (Enhanced) is in effect your  policy cannot lapse. Your Policy Protection Rider (Enhanced)  will lapse when the Net Policy Protection Value is equal to zero.  The minimum payment amount required (by the policy anniversary date) to  maintain a positive net Policy Protection Value until your next  anniversary Aug 1 2020 is $0.00.  Policy loans withdrawals or changes in benefits will cause this amount  to change. This rider cannot be reinstated once it has terminated.  Your Net Policy Protection Value will equal zero and your  Policy Protection Rider (Enhanced) will lapse prior to your  selected benefit period if insufficient premiums are paid and/or  if premiums are paid after the premium due date. If you have not  been paying your planned premium or if you have made your premium  payments after the premium due date please contact our Customer  Service Center at 1-800-387-2747 to request an Inforce Illustration  and to discuss the impact that this will have on your  Policy Protection Rider (Enhanced).  If you have any questions about your Policy Protection Rider (Enhanced)  please review the Policy Protection Rider (Enhanced)  section of your contract or contact your John Hancock Representative  listed on this annual statement.  Page 3 of 8  www.jhlifeinsurance.com \n Page Num   4 \n  Page Num   5 \n WELCOME FUNDS INC.  FUNDS INC.  LUJNAUTHORIZED USE STRICTLY PRO INDITED  Your Policy Annual Statement  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  Policy Number: 59 710 467  It is important to us that you have the best possible information about  your policy as it is one of your most valuable assets.  If you have any questions or need service of any kind please contact  John Hancock (U.S.A.)  Life Post Issue-Customer Service Center  PO Box 55979  Boston MA 02205  Phone: 1-800-387-2747  We look forward to continuing to serve your financial planning needs.  Page 4 of 8  www.jhlifeinsurance.com \n Page Num   5 \n  Page Num   6 \n WELCOME FUNDS INC.  Johnskuncock  FUNDS INC. Your LIJNAUTHORIZED Policy Annual USE STRICTI Statement Y PROHIBITED  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  Policy Number: 59 710 467  SUPPLEMENTARY BENEFITS  The following supplementary benefits are included in your contract  Page 5 of 8  www.jhlifeinsurance.com \n Page Num   6 \n  Page Num   7 \n John Han  WELCOME FUNDS INC.  PRODERTY Hancoek. WELCOME FUNDS INC: LUUNAUITHORIZED USE STRICTLY PROHIBITED  Your Policy Annual Sta Cement  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  POLICY NUMBER : 59 710 467  DETAILED RECORD OF TRANSACTIONS 08/02/18 TO 08/01/19  STATEMENT DATE: 08/02/19  PROCESS DATE EFFECTIVE DATE  TRANSACTION  POLICY  TRANSACTION  AMOUNT  VALUE  08/02/18  08/02/18  OPENING BALANCE  504811.97  08/02/18  08/02/18  COST OF INSURANCE  702.63-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  503509.62  09/04/18  09/02/18  INTEREST  1824.20  COST OF INSURANCE  702.32-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  504031.78  10/02/18  10/02/18  INTEREST  1767.08  COST OF INSURANCE  702.04-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  504497.10  11/02/18  11/02/18  INTEREST  1827.78  COST OF INSURANCE  701.73-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  505023.43  12/03/18  12/02/18  INTEREST  1770.56  Page 6 of 8  www.jhlifeinsurance.com \n Page Num   7 \n  Page Num   8 \n WELCOME FUNDS INC.  Hancock/ELCOME FUNDS INC.  LUJNAUTHORIZED USE STRICTI Y PROHIBITED  Your Policy Annual Statement  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  POLICY NUMBER : 59 710 467  DETAILED RECORD OF TRANSACTIONS 08/02/18 TO 08/01/19  STATEMENT DATE: 08/02/19  PROCESS DATE EFFECTIVE DATE  TRANSACTION  POLICY  TRANSACTION  AMOUNT  VALUE  12/03/18  12/02/18  COST OF INSURANCE  701.45-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  505492.82  01/02/19  01/01/19  INTEREST  1772.20  507265.02  01/02/19  01/02/19  INTEREST  59.18  COST OF INSURANCE  701.13-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  506023.35  02/04/19  02/02/19  INTEREST  1833.31  COST OF INSURANCE  700.82-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  506556.12  03/04/19  03/02/19  INTEREST  1652.67  COST OF INSURANCE  700.61-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  506908.46  04/02/19  04/02/19  INTEREST  1691.37  Page 7 of 8  www.jhlifeinsurance.com \n Page Num   8 \n  Page Num   9 \n WELCOME FUNDS INC.  John Hancock  FUNDS INC. Your ILINALTTHORIZEDUSE Policy Annual STRICTLY (Rstat cement PROHIBITED  JOHN HANCOCK LIFE INSURANCE  COMPANY (U.S.A.)  POLICY NUMBER : 59 710 467  DETAILED RECORD OF TRANSACTIONS 08/02/18 TO 08/01/19  STATEMENT DATE: 08/02/19  PROCESS DATE EFFECTIVE DATE  TRANSACTION  POLICY  TRANSACTION  AMOUNT  VALUE  04/02/19  04/02/19  COST OF INSURANCE  700.38-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  507299.73  05/02/19  05/02/19  INTEREST  1637.98  COST OF INSURANCE  700.18-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  507637.81  06/03/19  06/02/19  INTEREST  1693.80  COST OF INSURANCE  699.94-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  508031.95  07/02/19  07/02/19  INTEREST  1640.34  COST OF INSURANCE  699.74-  ADMINISTRATIVE CHARGE  20.00-  CONTRACT CHARGE  149.71-  COVERAGE EXPENSE CHARGE  143.79-  COST OF SUPPL. BENEFITS  286.22-  508372.83  08/02/19  08/02/19  INTEREST  1696.25  510069.08  Page 8 of 8  www.jhlifeinsurance.com \n Page Num   9 \n  Page Num   10 \n WELCOME FUNDS INC.  PROPER RTOOF WELCOME FUNDS INC.  John Hancock.  UNAUTHORIZED USE STRICTLY PROHIBITED  John Hancock Life Insurance Company (U.S.A.)  An Inforce Life Insurance Policy Illustration Snapshot Survivorship  Flexible Premium Adjustable Life Insurance Policy  Survivorship UL G  PHILLIP BAUM  1. Current policy year values (shown below as policy year 15) reflect the status of your policy  male age 69 non-smoker  as of August 2. 2019. All future values are projected based on these policy values.  preferred class  2. All illustrated values assume that premiums are paid as scheduled. Cash surrender values and  JOAN L BAUM  female age 68. non-smoker  death benefits are end of year values. Only those values labeled as guaranteed will be  standard class  contractually guaranteed in your policy. The annual guaranteed interest rate will not be less  than 3.00%. Guaranteed values also reflect maximum charges.  Policy #  5971046  Current Basic  $1691620  3. Illustrated scale values are not guaranteed and are based on current cost of insurance charges  Face Amount  Current Total  $1691620  and an interest rate of 4.00% which are both subject to change. Actual results may be more or  Death Benefit  less favorable.  4. Mid-point scale values are not guaranteed and are based on an interest rate cost of insurance  charges and any loan rates that are half way between the guaranteed and illustrated scales.  * The Policy Protection Rider Enhanced terminates in month 1 of year 33.  Guaranteed  Not Guaranteed  Not Guaranteed  at rate of of 3.00%  at mid-point scale (3.50%)  at illustrated scale (4.00%)  Net  Net cash  Net  Net  Net cash  Net  Net  Net cash  Net  Premiums  amount  surrender  death  amount  surrender  death  amount  surrender  death  Policy  you pay  you pay  value  benefit  you pay  value  benefit  you pay  value  benefit  year  ($)  ($)  ($)  ($)  ($)  ($)  ($)  ($)  ($)  ($)  15  0  0  438321  1691620  0  475954  1691620  0  512.619  1691620  20  0  0  0  1691620  0  18507  1691620  0  438635  1691620  25  0  0  0  1691620  0  0  1691620  0  52037  1691620  30  0  0  0  1691620  0  0  1691620  0  0  1691620  35  0  0  0  1691620  0  0  1691620  0  0  1691620  40  0  0  0  1691620  0  0  1691620  0  0  1691620  45  0  0  0  1691620  0  0  1691620  0  0  1691620  50  0  0  0  1691620  0  0  1691620  0  0  1691620  52  0  0  0  1691620  0  0  1691620  0  0  1691620  Your coverage ends in policy year  #  #  #  # See Age 100 Advantage  Form JS0700  @2019. John Hancock Life Insurance Company (U.S.A.). All rights reserved.  SUL04 (TK) Version 5.29 TN  Page 1 of 2 pages  Illustration #08052019073245  F-BBHG \n Page Num   10 \n  Page Num   11 \n WELCOME FUNDS INC.  PROP WF COME FUNDS INC.  UNAUTHORIZED USE STRICTLY PROHIBITED  John Hancock Life Insurance Company (U.S.A.)  An Inforce Life Insurance Policy Illustration Snapshot Survivorship  Flexible Premium Adjustable Life Insurance Policy  TERMS USED IN THIS ILLUSTRATION  Age 100 Advantage  Age 100 Advantage offers protection from the possibility of outliving coverage. Provided coverage is in effect  when the younger insured reaches attained age 100 or would have reached age 100 if living coverage will continue  after age 100 and interest will be credited but no additional charges other than those for any outstanding policy  loans will be deducted. The policy continues until second death.  Death Benefit Option  determines the amount of death benefit payable. The option is chosen by the policyholder at issue and may be  changed at a policy anniversary. Two options are available. Option 1 provides a level death benefit equal to the  face amount of the policy. Option 2 provides a death benefit equal to the face amount of the policy plus the policy  value.  Loan Interest  is the interest charged on your policy loan. If you do not pay the loan interest it is added to your outstanding loan  balance. Any outstanding loan balance reduces the amount paid when the surviving insured dies or when you  surrender your policy.  Mid-Point Scale  Mid-point scale values are not guaranteed and are based on an interest rate cost of insurance charges and any loan  rates that are half way between the guaranteed and illustrated scales.  Net Amount You Pay  is the difference between premiums and any loan interest you pay and amounts you take out in loans and  withdrawals.  Net Cash Surrender Value  is the money you will receive if you terminate the policy. The amount is the policys value minus the surrender  charge and any outstanding loans loan interest and monthly deductions.  Net Death Benefit  is the death benefit less any loans and loan interest.  Premiums you pay  are the amount of premiums we assume you will pay out-of-pocket.  Risk Classification  reflects the underwriting classifications being placed on your policy as assessed during the underwriting process  due to health occupational or recreational activities. The rate classes can be divided into two major categories  Smoker and Non-smoker each of which contains three general categories. From most to least favorable these  categories are Preferred Standard and Rated. The premium will be based on the final underwriting assessment.  Surrender Charge  is the amount deducted from the policy value in the event that you surrender the policy for cash or if it terminates at  the end of a grace period during the surrender charge period. The surrender charge period varies based on the age  of the younger insured.  WHAT THIS INFORCE ILLUSTRATION TELLS YOU  We have created this inforce illustration using information we have on file regarding your policy. It is based on your total current annualized premium. In  addition the values shown reflect any loans or withdrawals you may have taken. The Death Benefit Option being illustrated is Option 1 which is a level  death benefit option.  It is important to keep in mind that this is an inforce illustration only. This inforce illustration is intended to provide you a snapshot of your policy using  conditions which exist today; it is not intended to predict future performance.  OTHER IMPORTANT INFORMATION  This inforce illustration is not a contract. We suggest you refer to your policy for a complete explanation of your policy benefits. If you have any  questions regarding your policy or this inforce illustration our Customer Service Representatives would be pleased to assist you at  1-800-387-2747.  Tax implications: This inforce illustration may not reflect your actual tax situation. If you have questions regarding the tax implications of this policy we  recommend you discuss these with your tax advisor.  Form JS0700  SUL04 (TK) Version 5.29 TN  ©2019. John Hancock Life Insurance Company (U.S.A). All rights reserved.  Page 2 of 2 pages  Illustration #08052019073245  F-BBHG \n"

    text_size_bytes = len(DetectSentimenttext.encode('utf-8'))
    sentiment = []
    dominant_language = []
    entities = []
    DetectKeyPhrases = []
    pii_entities = []
    DetectSyntax = []
    max_text_size = 5000
    if text_size_bytes <= max_text_size:
        response = comprehend.detect_sentiment(Text=DetectSentimenttext, LanguageCode='en')
        sentiment = response['Sentiment']
        print(f"Sentiment: {sentiment}")
    else:
        chunks = [DetectSentimenttext[i:i+max_text_size] for i in range(0, len(DetectSentimenttext), max_text_size)]
        for chunk in chunks:
            response = comprehend.detect_sentiment(Text=chunk, LanguageCode='en')
            sentiment.append(response['Sentiment'])

            res_dominant_language = comprehend.detect_dominant_language(Text = chunk)
            dominant_language.append(res_dominant_language['Languages'])

            res_entities = comprehend.detect_entities(Text=chunk, LanguageCode='en')
            entities.append(res_entities['Entities'])

            res_DetectKeyPhrases = comprehend.detect_key_phrases(Text=chunk, LanguageCode='en')
            DetectKeyPhrases.append(res_DetectKeyPhrases['KeyPhrases'])

            res_pii_entities = comprehend.detect_pii_entities(Text=chunk, LanguageCode='en')
            pii_entities.append(res_pii_entities['Entities'])

            res_DetectSyntax = comprehend.detect_syntax(Text=chunk, LanguageCode='en')
            DetectSyntax.append(res_DetectSyntax['SyntaxTokens'])

        overAllinfo = {
             "DetectSyntax": DetectSyntax,
            "pii_entities": pii_entities,
            "DetectKeyPhrases": DetectKeyPhrases,
            "dominant_language": dominant_language,
            "sentiment": sentiment,
            "entities": entities,
        }
        # df = pd.DataFrame(entities)
        # print(FilePath +'outputoverData.xlsx')
        # print(FilePath)

        # # Step 3: Export DataFrame to Excel file
        # df.to_excel(FilePath +'outputoverData.xlsx', index=False)  # Set index=False to exclude row numbers in Excel

        # print("Conversion completed. Excel file saved as 'output.xlsx'.")
        # Convert "pii_entities" to DataFrame
        pii_data = []
        for entity_list in overAllinfo["pii_entities"]:
            for item in entity_list:
                pii_data.append(item)

        pii_df = pd.DataFrame(pii_data)

        # Convert "DetectSyntax" to DataFrame
        syntax_data = []
        for syntax_list in overAllinfo["DetectSyntax"]:
            for item in syntax_list:
                syntax_data.append(item)

        syntax_df = pd.DataFrame(syntax_data)
        # Convert "DetectKeyPhrases" to DataFrame
        DetectKeyPhrases_data = []
        for DetectKeyPhrases_list in overAllinfo["DetectKeyPhrases"]:
            for item in DetectKeyPhrases_list:
                DetectKeyPhrases_data.append(item)

        DetectKeyPhrases_df = pd.DataFrame(DetectKeyPhrases_data)

        # Convert "dominant_language" to DataFrame
        dominant_language_data = []
        for dominant_language_list in overAllinfo["dominant_language"]:
            for item in dominant_language_list:
                dominant_language_data.append(item)

        dominant_language_df = pd.DataFrame(dominant_language_data)
        # Convert "sentiment" to DataFrame
        sentiment_data = []
        for sentiment_list in overAllinfo["sentiment"]:
            for item in sentiment_list:
                sentiment_data.append(item)

        sentiment_df = pd.DataFrame(sentiment_data)
        # Convert "DetectKeyPhrases" to DataFrame
        entities_data = []
        for entities_list in overAllinfo["entities"]:
            for item in entities_list:
                entities_data.append(item)

        entities_df = pd.DataFrame(entities_data)

        # Save the DataFrames to an Excel file with multiple sheets
        # output_file = FilePath +"output1.xlsx"
        # kvoutput_txt = FilePath_1 + tempfilename + "_comprehend.csv"
        # print("kvoutput_txt",kvoutput_txt)
        # with pd.ExcelWriter(kvoutput_txt) as writer:
        #     entities_df.to_excel(writer, sheet_name='Entities', index=False)
        #     sentiment_df.to_excel(writer, sheet_name='Sentiment', index=False)
        #     pii_df.to_excel(writer, sheet_name='Pii Entities', index=False)
        #     syntax_df.to_excel(writer, sheet_name='DetectSyntax', index=False)
        #     DetectKeyPhrases_df.to_excel(writer, sheet_name='Detect Key Phrases', index=False)
        #     dominant_language_df.to_excel(writer, sheet_name='Dominant Language', index=False)
        # Save DataFrames to CSV files

        kvoutput_pii_entities = FilePath_1 + tempfilename + "pii_entities.csv"
        kvoutput_Sentiment = FilePath_1 + tempfilename + "Sentiment.csv"
        kvoutput_sentiment_df = FilePath_1 + tempfilename + "sentiment_df.csv"
        kvoutput_Entities = FilePath_1 + tempfilename + "Entities.csv"
        kvoutput_Detect_Key_Phrases = FilePath_1 + tempfilename + "Detect_Key_Phrases.csv"
        kvoutput_dominant_language_df = FilePath_1 + tempfilename + "dominant_language_df.csv"


        pii_df.to_csv(FilePath_1 + tempfilename + 'pii_entities.csv', index=False)
        syntax_df.to_csv(FilePath_1 + tempfilename + 'Sentiment.csv', index=False)
        sentiment_df.to_csv(FilePath_1 + tempfilename + 'sentiment_df.csv', index=False)
        entities_df.to_csv(FilePath_1 + tempfilename + 'Entities.csv', index=False)
        DetectKeyPhrases_df.to_csv(FilePath_1 + tempfilename + 'Detect_Key_Phrases.csv', index=False)
        dominant_language_df.to_csv(FilePath_1 + tempfilename + 'dominant_language_df.csv', index=False)
            
        pii_entities = path+"/"+ tempfilename+"/"+tempfilename+"pii_entities.csv"
        Sentiment = path+"/"+ tempfilename+"/"+tempfilename+"Sentiment.csv"
        sentiment_df = path+"/"+ tempfilename+"/"+tempfilename+"sentiment_df.csv"
        Entities = path+"/"+ tempfilename+"/"+tempfilename+"Entities.csv"
        Detect_Key_Phrases = path+"/"+ tempfilename+"/"+tempfilename+"Detect_Key_Phrases.csv"
        dominant_language_df = path+"/"+ tempfilename+"/"+tempfilename+"dominant_language_df.csv"
        # print("object_key",object_key)
        s3_client.upload_file(kvoutput_pii_entities, bucket_name, pii_entities)
        s3_client.upload_file(kvoutput_Sentiment, bucket_name, Sentiment)
        s3_client.upload_file(kvoutput_sentiment_df, bucket_name, sentiment_df)
        s3_client.upload_file(kvoutput_Entities, bucket_name, Entities)
        s3_client.upload_file(kvoutput_Detect_Key_Phrases, bucket_name, Detect_Key_Phrases)
        s3_client.upload_file(kvoutput_dominant_language_df, bucket_name, dominant_language_df)

        # print(f"Data has been successfully converted and saved to '{kvoutput_txt}'.")
        print("Data has been successfully converted and saved to CSV files.")



    return JsonResponse({
        "DetectSyntax": DetectSyntax,
        "pii_entities": pii_entities,
        "DetectKeyPhrases": DetectKeyPhrases,
        "dominant_language": dominant_language,
        "sentiment": sentiment,
        "entities": entities,
        "errorCode": 200,
        "errorMsg": "success"
    }, status=200)