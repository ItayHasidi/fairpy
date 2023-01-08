#include <string>
#include <vector>
using namespace std;

std::vector<std::vector<std::string>> H_M_l(std::vector<std::vector<std::string>> agents, std::vector<std::string> items, int level){
    std::vector<std::vector<std::string>> h_m_l = {};

    return h_m_l;
}

bool have_different_elements(std::vector<std::vector<std::string>> H_M){
    bool have_different = false; 

    return have_different;
}

std::vector<std::vector<std::string>> deep_copy_2d_vector(std::vector<std::vector<std::string>> lst){
    std::vector<std::vector<std::string>> lst_copy = {};

    return lst_copy;
}

void allocate(){
    
}


std::vector<std::vector<std::vector<std::string>>> sequential(std::vector<std::vector<std::string>> agents, std::vector<std::string> items, std::vector<std::vector<std::string>> allocations, std::vector<std::vector<std::vector<std::string>>> end_allocations, int level){
    if(items.empty()){
        std::vector<std::string> temp_allocation_alice = allocations[0];
        std::vector<std::string> temp_allocation_george = allocations[1];
        end_allocations.push_back({temp_allocation_alice, temp_allocation_george});
        return end_allocations;
    }
    std::vector<std::vector<std::string>> H_M= H_M_l(agents, items, level);
    if(!H_M[0].empty() && !H_M[1].empty() && have_different_elements(H_M)){
        for(int i = 0; i < sizeof(H_M[0]); i++){
            for(int j = 0; j < sizeof(H_M[1]); j++){
                if(i != j){
                    std::vector<std::vector<std::string>> _allocations = deep_copy_2d_vector(allocations);

                }
            }
        }
    }
    return end_allocations;
}

