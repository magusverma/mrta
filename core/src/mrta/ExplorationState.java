package mrta;

import aima.core.agent.Action;
import aima.core.search.framework.Node;
import mrta.GridPosition;

import java.util.List;

public class ExplorationState {

    public List<GridPosition> robots;
    public List<GridPosition> targets;
    public boolean[][] gridCells;

    public ExplorationState(List<GridPosition> robots, List<GridPosition> targets, boolean[][] gridCells) {
        this.robots = robots;
        this.targets = targets;
        this.gridCells = gridCells;
    }
}
