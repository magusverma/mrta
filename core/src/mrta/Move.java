package mrta;

/**
 * Created by magusverma on 18/09/15.
 */
public enum Move {
    STAY(0,0), UP(-1,0), DOWN(1,0), LEFT(0,-1), RIGHT(0,1);


    int x_move, y_move;
    Move(int x_move, int y_move){
        this.x_move = x_move;
        this.y_move = y_move;
    }
}
