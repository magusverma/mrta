package mrta;

import aima.core.search.framework.GoalTest;

/**
 * Created by magusverma on 18/09/15.
 */
public class ExplorationGoalTest implements GoalTest {
    public boolean isGoalState(Object state_) {
        ExplorationState state = (ExplorationState) state_;
        return state.targets.size() == 0;
    }
}
