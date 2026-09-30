import automata.Automaton;
import automata.AutomatonSimulator;
import automata.SimulatorFactory;
import file.XMLCodec;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;
import java.util.Collections;

/** Executa os arquivos reais com o leitor e simulador do JFLAP. */
public class JflapRuntimeCheck {
    public static void main(String[] args) throws Exception {
        java.io.PrintStream report = System.out;
        // O JFLAP 7.1 imprime depuração de intervalos durante a simulação.
        System.setOut(new java.io.PrintStream(java.io.OutputStream.nullOutputStream()));
        int total = 0;
        int failures = 0;
        for (String name : new String[]{"ER-01", "ER-02", "ER-03", "ER-04", "ER-05", "ER-06"}) {
            File file = Path.of(args[0], "docs", "diagramas", name, name + ".jff").toFile();
            Automaton automaton = (Automaton) new XMLCodec().decode(file, Collections.emptyMap());
            AutomatonSimulator simulator = SimulatorFactory.getSimulator(automaton);
            int count = 0;
            int errors = 0;
            for (String line : Files.readAllLines(Path.of(args[1], name + ".tsv"))) {
                String[] fields = line.split("\t", -1);
                String input = new String(Base64.getDecoder().decode(fields[1]), StandardCharsets.UTF_8);
                boolean expected = fields[0].equals("1");
                if (simulator.simulateInput(input) != expected) {
                    if (errors < 5) System.err.println(name + " divergencia: " + line);
                    errors++;
                }
                count++;
            }
            report.println(name + ": " + count + " casos, " + errors + " divergencias");
            total += count;
            failures += errors;
        }
        report.println("JFLAP: " + total + " casos, " + failures + " divergencias");
        if (failures != 0) System.exit(1);
    }
}
