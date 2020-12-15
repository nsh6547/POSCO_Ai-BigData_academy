import util
import wordsegUtil


class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def start_state(self):
        return 0, wordsegUtil.SENTENCE_BEGIN  # position before which text is reconstructed & previous word

    def is_end(self, state):
        return state[0] == len(self.query)

    def succ_and_cost(self, state):
        list_results = []
        pos, prev_word = state
        for num in range(1, len(self.query) - pos + 1):
            collect = self.possibleFills(self.query[pos:pos+num])
            for word in collect:
                action = word
                n_state = (pos+num,word)
                cost = self.bigramCost(prev_word, word)
                list_results.append((action,n_state,cost))
                
        return list_results


if __name__ == '__main__':
    unigramCost, bigramCost = wordsegUtil.makeLanguageModels('leo-will.txt')
    smoothCost = wordsegUtil.smoothUnigramAndBigram(unigramCost, bigramCost, 0.2)
    possibleFills = wordsegUtil.makeInverseRemovalDictionary('leo-will.txt', 'aeiou')
    problem = JointSegmentationInsertionProblem('mgnllthppl', smoothCost, possibleFills)
    # problem = JointSegmentationInsertionProblem(wordsegUtil.removeAll('whatsup', 'aeiou'), smoothCost, possibleFills)

    # import dynamic_programming_search
    # dps = dynamic_programming_search.DynamicProgrammingSearch(verbose=1)
    # # dps = dynamic_programming_search.DynamicProgrammingSearch(memory_use=False, verbose=1)
    # print(dps.solve(problem))

    import uniform_cost_search
    ucs = uniform_cost_search.UniformCostSearch(verbose=0)
    print(ucs.solve(problem))


# === Other Examples ===
# 
# QUERIES_BOTH = [
#     'stff',
#     'hllthr',
#     'thffcrndprncndrw',
#     'thstffffcrndprncndrwmntdthrhrssndrdn',
#     'whatsup',
#     'ipovercarrierpigeon',
#     'aeronauticalengineering',
#     'themanwiththegoldeneyeball',
#     'lightbulbsneedchange',
#     'internationalplease',
#     'comevisitnaples',
#     'somethingintheway',
#     'itselementarymydearwatson',
#     'itselementarymyqueen',
#     'themanandthewoman',
#     'nghlrdy',
#     'jointmodelingworks',
#     'jointmodelingworkssometimes',
#     'jointmodelingsometimesworks',
#     'rtfclntllgnc',
# ]
