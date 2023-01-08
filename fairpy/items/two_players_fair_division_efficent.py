import cppyy

cppyy.cppdef("""
#include <string>
#include <vector>
using namespace std;

class ItemList{
    std::vector<std::string> items;

public:
    ItemList(){
        this->items = {};
    }

    ItemList(std::vector<std::string> items){
        this->items = items;
    }

    void clear_list(){
        this->items.clear();
    }

    std::vector<std::string> get_items(){
        return this->items;
    }

    void add_item(string item){
        this->items.push_back(item);
    }

    void remove_item(int idx){
        items.erase(items.begin() + idx);
    }
};

class ItemLists{
    ItemList listA, listB;

public:
    ItemLists(ItemList listA, ItemList listB){
        this->listA = listA;
        this->listB = listB;
    }
    
    ItemList get_ListA(){
        return this->listA;
    }
    
    ItemList get_ListB(){
        return this->listB;
    }
};

class Agent{
    std::string name;
    std::vector<std::string> items;
    std::vector<int> valuations;

public:
    Agent(){
        this->name = "";
        this->items = {};
        this->valuations = {};
    }

    Agent(std::string name, std::vector<std::string> items, std::vector<int> valuations){
        this->name = name;
        this->items = items;
        this->valuations = valuations;
    }

    Agent(Agent other){
        this->name = other.name;
        this->items = other.items;
        this->valuations = other.valuations;
    }

    std::string get_name(){
        return this->name;
    }

    std::vector<std::string> get_items(){
        return this->items;
    }

    std::vector<int> get_valuations(){
        return this->valuations;
    }

    void remove_item(int idx){
        items.erase(items.begin() + idx);
        valuations.erase(valuations.begin() + idx);
    }
};

class AgentList{
    Agent agentA, agentB;

public:
    AgentList(Agent agentA, Agent agentB){
        this->agentA = Agent(agentA);
        this->agentB = Agent(agentB);
    }

    Agent get_AgentA(){
        return this->agentA;
    }

    Agent get_AgentB(){
        return this->agentB;
    }
};


std::string find_last_item(Agent agent, ItemList item_list){
    int max_score = -1;
    std::string max_item = "";
    for(int i = 0; i < sizeof(item_list.get_items()); i++){
        int score = agent.get_valuations()[i];
        if(max_score < score){
            max_score = score;
            max_item = agent.get_items()[i];
        }
    }
    return max_item;
}

std::vector<ItemList> deep_copy_2d_list(std::vector<ItemList> lst){
    std::vector<ItemList> lst_copy;
    for(int i = 0; i < sizeof(lst); i++){
        ItemList tempList;
        for(int j = 0; j < sizeof(lst[i].get_items()); j++){
            tempList.add_item(lst[i].get_items()[j]);
        }
        lst_copy.push_back(tempList);
        tempList.clear_list();
    }
    return lst_copy;
}
""")


