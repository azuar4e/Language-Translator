package procesador;

public class cuarteto {
    public String operador;
    public Object arg1;
    public Object arg2;
    public Object resultado;

    public cuarteto(String operador, Object arg1, Object arg2, Object resultado) {
        this.operador = operador;
        this.arg1 = arg1;
        this.arg2 = arg2;
        this.resultado = resultado;
    }

    @Override
    public String toString() {
        return "(" + operador + ", " + arg1 + ", " + arg2 + ", " + resultado + ")";
    }
}
