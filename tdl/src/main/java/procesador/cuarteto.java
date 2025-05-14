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
        if (arg1 instanceof gci.tupla){
            arg1 = arg1.toString();
        }
        if (arg1 == null){
            arg1 = "";
        }
        if (arg2 instanceof gci.tupla){
            arg2 = arg2.toString();
        }
        if (arg2 == null){
            arg2 = "";
        }
        if (resultado instanceof gci.tupla){
            resultado = resultado.toString();
        }
        if (resultado == null){
            resultado = "";
        }
        return "(" + operador + ", " + arg1 + ", " + arg2 + ", " + resultado + ")\n";
    }
}
