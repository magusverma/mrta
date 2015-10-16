#include <bits/stdc++.h>
#define ll long long int 
#define getc getchar_unlocked
using namespace std;

struct position{
    int row, col;

    void copy(struct position p){
        row = p.row;
        col = p.col;
    }
};
typedef struct position position;

vector<vector<bool> > grid;
// (0,0) (0,1) (0,2)
// (1,0) (1,1) (1,2)

vector<position> targets;
ll width, height;


struct state{
    vector<position> robots;
    int total_picked;
    vector<bool> picked;
    string solution_;

    void pick(int i){
        if(picked[i]==false){
            picked[i] = true;
            total_picked += 1;
        }
    }

    void copy(state s){
        robots.resize(s.robots.size());
        for (int i = 0; i < s.robots.size(); ++i)
        {
            robots[i].copy(s.robots[i]);
        }
        total_picked = s.total_picked;
        picked.resize(s.picked.size());
        for (int i = 0; i < s.picked.size(); ++i)
        {
            picked[i] = s.picked[i];
        }
    }

    string getRep(){
        stringstream ss;
        for (int i = 0; i < robots.size(); ++i)
        {
            ss<<robots[i].row<<","<<robots[i].col<<" ";
        }
        for (int i = 0; i < picked.size(); ++i)
        {
            if (picked[i]){
                ss<<"T";
            }else{
                ss<<"F";
            }
        }
        return ss.str();
    }

    string getRobos(){
        stringstream ss;
        ss<<"[";
        for (int i = 0; i < robots.size(); ++i)
        {
            ss<<"["<<robots[i].row<<","<<robots[i].col<<"]";
            if(i!=robots.size()-1)ss<<",";
        }
        ss<<"]";
        return ss.str();
    }

};
typedef struct state state;

struct agent_move{
    int x_agent_move;
    int y_agent_move;
    // (-1,-1): left up
    // (-1,0): up
    // (-1,+1): right up
    // ...

    double cost(){
        double cost = (x_agent_move*x_agent_move);
        cost += (y_agent_move*y_agent_move);
        cost = sqrt(cost);
        return cost;
    }
    
};
typedef struct agent_move agent_move;

struct action{
    // move for every robot
    vector<agent_move> agent_moves;

    double cost(){
        double c = 0.0;
        for (int i = 0; i < agent_moves.size(); ++i)
        {
            c += agent_moves[i].cost();
        }
        return c;
    }
};
typedef struct action action;

// struct heap_element{
//     state s;
//     int g_val, h_val;
//     int f_val(){
//         return g_val+h_val;
//     }
// };
// typedef struct heap_element heap_element;

bool within_boundary(int x, int y){
    bool within_horizontal_bound = (0<=y && y<width);
    bool within_vertical_bound = (0<=x && x<height);
    return (within_horizontal_bound && within_vertical_bound);
}

bool movable(int row,int col){
    // lies outside grid
    if (!within_boundary(row,col)) return false;

    // if blocked in environment
    if (grid[row][col]) return false;
    
    // not blocked
    return true;
}

bool reached_limit(vector<int> current, vector<int> limit){
    for (int i = 0; i < current.size(); ++i)
    {
        if(current[i]!=limit[i]-1)
            return false;
    }
    return true;
}
vector<int> increment(vector<int> current, vector<int> limit){
    for (int i = current.size()-1; i >= 0; --i)
    {
        if (current[i] < limit[i]-1){
            current[i] +=1;
            break;
        }
        current[i] = 0;
    }
    return current;
}

bool validate_transition(state s, action a){
    bool marked[width][height];
    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            marked[i][j] = false;
        }
    }

    // check if two robots going to step in on same cell
    for (int i = 0; i < s.robots.size(); ++i)
    {
        if(marked[s.robots[i].row+a.agent_moves[i].x_agent_move][s.robots[i].col+a.agent_moves[i].y_agent_move])
            return false;
        marked[s.robots[i].row+a.agent_moves[i].x_agent_move][s.robots[i].col+a.agent_moves[i].y_agent_move] = true;
    }
    return true;
}

vector<action> get_possible_actions(state s){
    vector<action> possible_actions;

    vector<vector<agent_move> > possible_agent_moves_per_robot;
    vector<int> base, limit;

    for (int i = 0; i < s.robots.size(); ++i)
    {
        position robot;
        robot.copy(s.robots[i]);
        vector<agent_move> v;
        for (int i = -1; i <= 1; ++i)
        {
            for (int j = -1; j <= 1; ++j)
            {
                // if(i==0 &&j==0) continue;
                if(movable(robot.row + i, robot.col + j)){
                    agent_move m;
                    m.x_agent_move = i;
                    m.y_agent_move = j;
                    v.push_back(m);
                }
            }
        }  
        possible_agent_moves_per_robot.push_back(v);  
        base.push_back(0);
        limit.push_back(v.size());
    }

    while(true){
        // cout<<base[0]<<" "<<limit[0]<<endl;
        action a;
        for (int i = 0; i < s.robots.size(); ++i)
        {
            a.agent_moves.push_back(possible_agent_moves_per_robot[i][base[i]]);
        }
        if(validate_transition(s,a)){
            possible_actions.push_back(a);
        }
        if(reached_limit(base,limit))break;
        base = increment(base,limit);
    }

    // Printing action sequences for debugging purpose
    // for (int i = 0; i < possible_actions.size(); ++i)
    // {
    //     action a = possible_actions[i];
    //     cout<<"Possible Action Sequence "<<i+1<<endl;
    //     for (int j = 0; j < a.agent_moves.size(); ++j)
    //     {
    //         cout<<a.agent_moves[j].x_agent_move<<","<<a.agent_moves[j].y_agent_move<<" ";
    //     }
    //     cout<<endl;
    // }

    return possible_actions;
}

state transition(state s, action a){
    state new_state;
    // new_state.parent = &s;
    // cout<<"Parent Set as: "<<(*(new_state.parent)).getRep()<< " For:"<<new_state.getRep()<<endl;

    new_state.copy(s);

    for (int i = 0; i < new_state.robots.size(); ++i)
    {
        new_state.robots[i].row += a.agent_moves[i].x_agent_move;
        new_state.robots[i].col += a.agent_moves[i].y_agent_move;
    }
    for (int i = 0; i < new_state.robots.size(); ++i)
    {
        for (int j = 0; j < targets.size(); ++j)
        {
            if(new_state.robots[i].row == targets[j].row and new_state.robots[i].col == targets[j].col){
                new_state.pick(j);
            }
        }
    }
    new_state.solution_ = s.solution_+","+new_state.getRobos();    
    // cout<<"-Parent Set as: "<<(*(new_state.parent)).getRep()<< " For:"<<new_state.getRep()<<endl;
    return new_state;
}

// shubhorup
ll heuristic(state current){
    ll h_val = 0;
    // compute h_val
    // all possible allocation
    // cost of each allocation, by summing heuristic on tsp
    // return min of such sums
    return h_val;
}

bool goal_check(state current){
    return targets.size()==current.total_picked;
}

class Comparator
{
    public:
    int operator() ( const pair<state,double>& p1, const pair<state,double> &p2)
    {
        return p1.second>p2.second;
    }
};

// The functions parseLine and getValue have been taken from http://stackoverflow.com/questions/63166/how-to-determine-cpu-and-memory-consumption-from-inside-a-process
// and are used for finding the memory consumed
int parseLine(char* line){
        int i = strlen(line);
        while (*line < '0' || *line > '9') line++;
        line[i-3] = '\0';
        i = atoi(line);
        return i;
    }

int getValue(){ //Note: this value is in KB!
    FILE* file = fopen("/proc/self/status", "r");
    int result = -1;
    char line[128];

    while (fgets(line, 128, file) != NULL){
        if (strncmp(line, "VmSize:", 7) == 0){
            result = parseLine(line);
            break;
        }
    }
    fclose(file);
    return result;
}

#include <sys/time.h>
#include <sys/resource.h>

long getMemoryUsage() 
{
  struct rusage usage;
  if(0 == getrusage(RUSAGE_SELF, &usage))
    return usage.ru_maxrss; // bytes
  else
    return 0;
}


pair<state, double> dijkstra(state start_state){
    ll states_expanded = 0;
    ll memory=0;
    clock_t begin = clock();

    std::map<std::string,double > visited;
    priority_queue<pair<state, double>, vector<pair<state, double> >, Comparator> Heap;

    start_state.solution_ = "["+start_state.getRobos();

    Heap.push(make_pair(start_state,0));  
    
    while(!Heap.empty())
    {
        state current_state = Heap.top().first;
        double cost = Heap.top().second;
        Heap.pop();

        // safety exits
        memory=max(memory,(long long)getMemoryUsage()/1024);
        clock_t end = clock();
        double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
        if(memory/1024 > 500){
            cout<<cost<<" "<<states_expanded<<" "<<time_spent<<" "<<memory<<" KB OOM\n";
            return make_pair(current_state, cost);
        }
        if(time_spent>2){
            cout<<cost<<" "<<states_expanded<<" "<<time_spent<<" "<<memory<<" KB TLE\n";
            return make_pair(current_state, cost);
        }
        //

        // struct state *parent = (current_state.parent);
        // if(parent != NULL)
        // cout<<"Coming Fr "<<(*(parent)).getRep()<<endl;
        // else
        // cout<<"No Parent"<<endl;
            // cout<<"Solution  "<<current_state.solution_<<endl;
        
        if(goal_check(current_state)){
            // cout<<"Reached G "<<current_state.getRep()<< " cost="<<cost<<endl;
            // clock_t end = clock();
            // double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
 
            cout<<cost<<" "<<states_expanded<<" "<<time_spent<<" "<<memory<<" KB\n";
            return make_pair(current_state, cost);
        }
        // check if already expanded
        else if (visited.find(current_state.getRep()) != visited.end()){
            // cout<<"Avoiding  "<<current_state.getRep()<< " cost="<<cost<<" , as already expanded for cost "<<visited[current_state.getRep()]<<endl;
        }
        else{
            // cout<<"Expanding "<<current_state.getRep()<<" cost="<<cost<<endl;
            states_expanded +=1;

            visited[current_state.getRep()] = cost;
            vector<action> actions_ = get_possible_actions(current_state);
            for (int i = 0; i < actions_.size(); ++i)
            {
                state transitioned_state = transition((current_state), actions_[i]);
                double g = cost+actions_[i].cost();
                double f = g;
                Heap.push(make_pair(transitioned_state, f));
            }
        }
        // cout<<endl;
    }

    return make_pair(start_state, 0);
}

void print_state(state x){
    cout << " == CURRENT STATE == \n";
    char g[height][width];
    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            if(!grid[i][j]){
                g[i][j] = '-';
            }
        }
    }
    for (int i = 0; i < x.robots.size(); ++i)
    {
        cout<<"("<<x.robots[i].row<<" , "<<x.robots[i].col<<")";
        g[x.robots[i].row][x.robots[i].col] = 'R';
    }
    cout<<endl;

    for (int i = 0; i < targets.size(); ++i)
    {
        cout<<"("<<targets[i].row<<" , "<<targets[i].col<<")";
        if(!x.picked[i]){
            g[targets[i].row][targets[i].col] = 'T';    
        }
    }
    cout<<endl;
    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            if(grid[i][j]){
                g[i][j] = '*';
            }
        }
    }
    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {

            cout<<g[i][j];
        }
        cout<<endl;
    }
    // return g;
}

state takeInput(){
    cin>>height>>width;
    char g[height][width];
    for (int i = 0; i < height; ++i)
    {
        cin>>g[i];
    }

    state start;
    start.total_picked = 0;

    for (int i = 0; i < height; ++i)
    {
        vector<bool> row(width);
        for (int j = 0; j < width; ++j)
        {
            // cout<<g[i][j];
            
            if(g[i][j]=='*'){
                row[j] = true;
            }
            else{
                row[j] = false;
            }
            switch(g[i][j]){
                case 'R':
                    position robot_position;
                    robot_position.row = i;
                    robot_position.col = j;
                    start.robots.push_back(robot_position);
                    break;
                case 'T':
                    position target_position;
                    target_position.row = i;
                    target_position.col = j;
                    targets.push_back(target_position);
                    start.picked.push_back(false);
                    break;
            }
        }
        grid.push_back(row);
        // cout<<endl;
    }
    return start;
}
int main(){
    state start_state = takeInput();
    // cout<<"Computing";
    // print_state(start_state);
    pair<state, double> goal = dijkstra(start_state);
    cout<<goal.first.solution_+"]"<<endl;

    return 0;
}