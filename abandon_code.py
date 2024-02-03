            # # 處理每個字
            # self.old_word_list[indx]["each_T"] = []
            # self.old_word_list[indx]["each_T"].append({})
            # i = 0
            # self.old_word_list[indx]["each_T"][i]["eng"] = self.old_word_list[indx]["eng"]
            # del(self.old_word_list[indx]["eng"])
            # self.old_word_list[indx]["each_T"][i]["chi"] = self.old_word_list[indx]["chi"]
            # del(self.old_word_list[indx]["chi"])
            # self.old_word_list[indx]["each_T"][i]["status"] = self.old_word_list[indx]["status"]
            # del(self.old_word_list[indx]["status"])
            # self.old_word_list[indx]["each_T"][i]["date"] = self.old_word_list[indx]["date"]
            # del(self.old_word_list[indx]["date"])

            # for each_other in self.old_word_list[indx]["other"] :
            #     i += 1
            #     self.old_word_list[indx]["each_T"].append({})
            #     each_other_split = each_other.split(" ")
            #     if len(each_other_split) > 2 :
            #         print(each_other_split)
            #     if each_other_split[0].isalpha() :
            #         self.old_word_list[indx]["each_T"][i]["eng"] = each_other_split[0]
            #         self.old_word_list[indx]["each_T"][i]["chi"] = " ".join(each_other_split[1:])
            #     else :
            #         self.old_word_list[indx]["each_T"][i]["eng"] = each_other_split[-1]
            #         self.old_word_list[indx]["each_T"][i]["chi"] = " ".join(each_other_split[:-1])
            #     self.old_word_list[indx]["each_T"][i]["status"] = 0
            #     self.old_word_list[indx]["each_T"][i]["date"] = "2099/12/31"