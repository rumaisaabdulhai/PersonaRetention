import os
import json

'''
Percent Correct - Therapist:  0.9493087557603687
Percent Neutral - Therapist:  0.0
Percent Wrong - Therapist:  0.05069124423963134
Average Score - Therapist 0.8986175115207373
Percent Correct - Patient:  0.847926267281106
Percent Neutral - Patient:  0.016129032258064516
Percent Wrong - Patient:  0.1359447004608295
Average Score - Patient 0.7119815668202765
'''

'''
Percent Correct - Buyer:  0.002564102564102564
Percent Neutral - Buyer:  0.017948717948717947
Percent Wrong - Buyer:  0.9794871794871794
Average Score - Buyer -0.9769230769230769
Percent Correct - Seller:  0.9076923076923077
Percent Neutral - Seller:  0.010256410256410256
Percent Wrong - Seller:  0.08205128205128205
Average Score - Seller 0.8256410256410256
'''

'''
Percent Correct - Chitchat 1:  0.8874878758486906
Percent Neutral - Chitchat 1:  0.03685741998060136
Percent Wrong - Chitchat 1:  0.07565470417070805
Average Score - Chitchat 1 0.8118331716779825
Percent Correct - Chitchat 2:  0.9030067895247332
Percent Neutral - Chitchat 2:  0.030067895247332686
Percent Wrong - Chitchat 2:  0.06692531522793405
Average Score - Chitchat 2 0.8360814742967992
'''

# path_to_tp_evals = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tp_persona_consistency_eval.json'))
# path_to_bs_evals = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bs_persona_consistency_eval.json'))
path_to_chitchat_evals = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'chitchat_persona_consistency_eval.json'))

# with open(path_to_tp_evals, 'r') as f:
#     tp_eval_data = json.load(f)

# with open(path_to_bs_evals, 'r') as f:
#     bs_eval_data = json.load(f)

with open(path_to_chitchat_evals, 'r') as f:
    chitchat_eval_data = json.load(f)

correct_therapist = 0
neutral_therapist = 0
wrong_therapist = 0

correct_patient = 0
neutral_patient = 0
wrong_patient = 0

correct_buyer = 0
neutral_buyer = 0
wrong_buyer = 0

correct_seller = 0
neutral_seller = 0
wrong_seller = 0

correct_chitchat1 = 0
neutral_chitchat1 = 0
wrong_chitchat1 = 0

correct_chitchat2 = 0
neutral_chitchat2 = 0
wrong_chitchat2 = 0


# for filename, contents in bs_eval_data.items():
#     parts = filename.split("_")
#     if parts[0] == "therapist":
#         for item in contents['results']:
#             if item["role"] == "Therapist":
#                 if item["score"] == 1:
#                     correct_therapist += 1
#                 elif item["score"] == 0:
#                     neutral_therapist += 1
#                 elif item["score"] == -1:
#                     wrong_therapist += 1

#             elif item["role"] == "Patient":
#                 if item["score"] == 1:
#                     correct_patient += 1
#                 elif item["score"] == 0:
#                     neutral_patient += 1
#                 elif item["score"] == -1:
#                     wrong_patient += 1
#     elif parts[0] == "buyer":
#         for item in contents['results']:
#             if item["role"] == "Buyer":
#                 if item["score"] == 1:
#                     correct_buyer += 1
#                 elif item["score"] == 0:
#                     neutral_buyer += 1
#                 elif item["score"] == -1:
#                     wrong_buyer += 1

#             elif item["role"] == "Seller":
#                 if item["score"] == 1:
#                     correct_seller += 1
#                 elif item["score"] == 0:
#                     neutral_seller += 1
#                 elif item["score"] == -1:
#                     wrong_seller += 1


for filename, contents in chitchat_eval_data.items():
    parts = filename.split("_")
    if parts[0] == "chitchat":
        for item in contents['results']:
            if item["role"] == "Person 1":
                if item["score"] == 1:
                    correct_chitchat1 += 1
                elif item["score"] == 0:
                    neutral_chitchat1 += 1
                elif item["score"] == -1:
                    wrong_chitchat1 += 1

            elif item["role"] == "Person 2":
                if item["score"] == 1:
                    correct_chitchat2 += 1
                elif item["score"] == 0:
                    neutral_chitchat2 += 1
                elif item["score"] == -1:
                    wrong_chitchat2 += 1

# print("Percent Correct - Therapist: ", correct_therapist / (correct_therapist + wrong_therapist + neutral_therapist))
# print("Percent Neutral - Therapist: ", neutral_therapist / (correct_therapist + wrong_therapist + neutral_therapist))
# print("Percent Wrong - Therapist: ", wrong_therapist / (correct_therapist + wrong_therapist + neutral_therapist))

# print("Average Score - Therapist", (correct_therapist - wrong_therapist) / (correct_therapist + wrong_therapist + neutral_therapist))


# print("Percent Correct - Patient: ", correct_patient / (correct_patient + wrong_patient + neutral_patient))
# print("Percent Neutral - Patient: ", neutral_patient / (correct_patient + wrong_patient + neutral_patient))
# print("Percent Wrong - Patient: ", wrong_patient / (correct_patient + wrong_patient + neutral_patient))

# print("Average Score - Patient", (correct_patient - wrong_patient) / (correct_patient + wrong_patient + neutral_patient))

# print("Percent Correct - Buyer: ", correct_buyer / (correct_buyer + wrong_buyer + neutral_buyer))
# print("Percent Neutral - Buyer: ", neutral_buyer / (correct_buyer + wrong_buyer + neutral_buyer))
# print("Percent Wrong - Buyer: ", wrong_buyer / (correct_buyer + wrong_buyer + neutral_buyer))

# print("Average Score - Buyer", (correct_buyer - wrong_buyer) / (correct_buyer + wrong_buyer + neutral_buyer))

# print("Percent Correct - Seller: ", correct_seller / (correct_seller + wrong_seller + neutral_seller))
# print("Percent Neutral - Seller: ", neutral_seller / (correct_seller + wrong_seller + neutral_seller))
# print("Percent Wrong - Seller: ", wrong_seller / (correct_seller + wrong_seller + neutral_seller))

# print("Average Score - Seller", (correct_seller - wrong_seller) / (correct_seller + wrong_seller + neutral_seller))


print("Percent Correct - Chitchat 1: ", correct_chitchat1 / (correct_chitchat1 + wrong_chitchat1 + neutral_chitchat1))
print("Percent Neutral - Chitchat 1: ", neutral_chitchat1 / (correct_chitchat1 + wrong_chitchat1 + neutral_chitchat1))
print("Percent Wrong - Chitchat 1: ", wrong_chitchat1 / (correct_chitchat1 + wrong_chitchat1 + neutral_chitchat1))

print("Average Score - Chitchat 1", (correct_chitchat1 - wrong_chitchat1) / (correct_chitchat1 + wrong_chitchat1 + neutral_chitchat1))

print("Percent Correct - Chitchat 2: ", correct_chitchat2 / (correct_chitchat2 + wrong_chitchat2 + neutral_chitchat2))
print("Percent Neutral - Chitchat 2: ", neutral_chitchat2 / (correct_chitchat2 + wrong_chitchat2 + neutral_chitchat2))
print("Percent Wrong - Chitchat 2: ", wrong_chitchat2 / (correct_chitchat2 + wrong_chitchat2 + neutral_chitchat2))

print("Average Score - Chitchat 2", (correct_chitchat2 - wrong_chitchat2) / (correct_chitchat2 + wrong_chitchat2 + neutral_chitchat2))



