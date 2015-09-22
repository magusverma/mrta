package mrta;

/**
 * Created by magusverma on 18/09/15.
 */
public class GridPosition {
    private Integer row;
    private Integer column;

    public GridPosition(Integer row, Integer column) {
        this.row = row;
        this.column = column;
    }

    public Integer getRow() {
        return row;
    }

    public Integer getColumn() {
        return column;
    }

    public void setRow(Integer row) {
        this.row = row;
    }

    public void setColumn(Integer column) {
        this.column = column;
    }

    public int manhattanDistance(GridPosition other){
        return Math.abs(this.getRow()-other.getRow()) + Math.abs(this.getColumn()-other.getColumn());
    }
}
