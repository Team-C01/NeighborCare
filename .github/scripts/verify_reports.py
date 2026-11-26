"""Require actual JUnit reports from both initialized stacks."""
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

def count_reports(reports):
    total = skipped = errors = 0
    database_skipped = False
    for report in reports:
        for case in ET.parse(report).getroot().iter("testcase"):
            total += 1
            skipped += case.find("skipped") is not None
            errors += case.find("failure") is not None or case.find("error") is not None
            if "DatabaseIntegrationTest" in case.get("classname", "") and case.find("skipped") is not None:
                database_skipped = True
    return total - skipped, skipped, errors, database_skipped

def main():
    summary = []
    output = {}
    checks = {
        "Backend": list(Path("backend/target/surefire-reports").glob("TEST-*.xml"))
                   + list(Path("backend/target/failsafe-reports").glob("TEST-*.xml")),
        "Frontend": [Path("frontend/test-results/junit.xml")],
    }
    failed = False
    for name, reports in checks.items():
        try:
            if not reports:
                raise OSError("Nessun report")
            executed, skipped, errors, database_skipped = count_reports(reports)
            print(f"{name}: eseguiti={executed}, falliti/errori={errors}, saltati={skipped}")
            output[name.lower()] = f"{executed - errors} superati, {errors} falliti/errori, {skipped} saltati"
            summary.append(f"| {name} | {executed - errors} | {errors} | {skipped} |")
            failed |= not executed or bool(errors)
            if name == "Backend" and os.environ.get("NEIGHBORCARE_DB_TESTS") == "true" and database_skipped:
                print("Test di integrazione PostgreSQL saltato nonostante il servizio attivo")
                failed = True
        except (OSError, ET.ParseError) as exc:
            print(f"{name}: report non disponibile o non valido: {exc}")
            output[name.lower()] = "Non disponibile"
            summary.append(f"| {name} | N/D | N/D | N/D |")
            failed = True
    if "--summary" in sys.argv:
        table = "\n".join(["## Risultati test JUnit", "", "| Stack | Superati | Falliti/errori | Saltati |", "| --- | ---: | ---: | ---: |", *summary, "", "N/D: report assente, non valido o test non eseguiti. Consultare il job per gli errori di build/avvio."])
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as stream:
                stream.write(table + "\n")
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a") as stream:
                for name, value in output.items():
                    stream.write(f"{name}={value}\n")
    return int(failed)

if __name__ == "__main__":
    sys.exit(main())
