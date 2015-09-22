package mrta;

import java.util.ArrayList;
import java.util.List;

import aima.core.environment.eightpuzzle.ManhattanHeuristicFunction;
import aima.core.search.framework.GraphSearch;
import aima.core.search.framework.Problem;
import aima.core.search.framework.Search;
import aima.core.search.framework.SearchAgent;
import aima.core.search.informed.AStarSearch;

/**
 * Created by magusverma on 18/09/15.
 */
public class Tester {
    public static void main(String[] args){
        try {
            List<GridPosition> robots = new ArrayList<>();
            List<GridPosition> targets  = new ArrayList<>();
            boolean[][] grid = {
                    {false, false, false, false, false, false, false, true},
                    {true,  false, false, false, false, false, false, true},
                    {true,  false, false, false, false, true,  true,  true},
                    {true,  false, false, false, false, true,  true,  true},
                    {false, true,  true,  true,  true,  true,  true,  false}
            };
            robots.add(new GridPosition(1,1));
            targets.add(new GridPosition(5,5));

            ExplorationState initialState = new ExplorationState(robots, targets, grid);

            Problem problem = new Problem(initialState,
                    MRTAFunctionsFactory.getActionsFunction(),
                    MRTAFunctionsFactory.getResultFunction(),
                    new ExplorationGoalTest());
            Search search = new AStarSearch(new GraphSearch(),
                    new ExplorationHeuristicFunction());
            SearchAgent agent = new SearchAgent(problem, search);
            System.out.println("DONE" + agent.getActions().size());

//            Assert.assertEquals(23, agent.getActions().size());
//            Assert.assertEquals("926",
//                    agent.getInstrumentation().getProperty("nodesExpanded"));
//            Assert.assertEquals("534",
//                    agent.getInstrumentation().getProperty("queueSize"));
//            Assert.assertEquals("535",
//                    agent.getInstrumentation().getProperty("maxQueueSize"));
        } catch (Exception e) {
            e.printStackTrace();
//            Assert.fail("Exception thrown");
        }

    }
}
