package mrta;

import aima.core.agent.Action;
import aima.core.environment.eightpuzzle.EightPuzzleBoard;
import aima.core.search.framework.ActionsFunction;
import aima.core.search.framework.ResultFunction;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Created by magusverma on 18/09/15.
 */
public class MRTAFunctionsFactory {
    private static ActionsFunction _actionsFunction = null;
    private static ResultFunction _resultFunction = null;

    public static ActionsFunction getActionsFunction() {
        if (null == _actionsFunction) {
            _actionsFunction = new EPActionsFunction();
        }
        return _actionsFunction;
    }

    public static ResultFunction getResultFunction() {
        if (null == _resultFunction) {
            _resultFunction = new EPResultFunction();
        }
        return _resultFunction;
    }

    private static class ExplorationAction implements  Action{

        public ArrayList<Move> moves = new ArrayList<>();

        public ExplorationAction(ArrayList<Move> moves) {
            this.moves = moves;
        }

        @Override
        public boolean isNoOp() {
            return false;
        }
    }
    private static class EPActionsFunction implements ActionsFunction {
        public Set<Action> actions(Object state_) {
            ExplorationState state = (ExplorationState) state_;

            System.out.println("Ji");
            Set<Action> actions = new LinkedHashSet<Action>();

            // TODO Generate all possible moves and add to actions
            ArrayList<Move> moves = new ArrayList<>();
            for(GridPosition robot : state.robots){
                moves.add(Move.RIGHT);
            }
            ExplorationAction explorationAction = new ExplorationAction(moves);
            actions.add(explorationAction);

            return actions;
        }
    }

    private static class EPResultFunction implements ResultFunction {
        public Object result(Object s, Action a) {
            ExplorationState state = (ExplorationState) s;
            ExplorationAction action = (ExplorationAction) a;

            for (int i = 0; i < state.robots.size() ; i++) {
                GridPosition robot = state.robots.get(i);
                Move move = action.moves.get(i);
                robot.setRow(robot.getRow() + move.y_move);
                robot.setColumn(robot.getColumn() + move.x_move);
            }
            return s;
        }
    }
}
