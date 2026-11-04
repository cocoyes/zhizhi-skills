// Development-only check against the actual runtime catalog; no model calls.
package main

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/cocoyes/zhizhi-agent-runtime/skill"
)

func main() {
	if len(os.Args) != 2 {
		log.Fatal("usage: runtimecheck <skills-root>")
	}
	ctx := context.Background()
	catalog := skill.NewCatalog(skill.CatalogOptions{})
	report, err := catalog.LoadRoot(ctx, os.Args[1])
	if err != nil {
		log.Fatalf("load skill root %q: %v", os.Args[1], err)
	}
	metadata := catalog.Metadata()
	if len(metadata) != 10 {
		log.Fatalf("catalog count: got %d, want 10", len(metadata))
	}
	for _, meta := range metadata {
		loaded, err := catalog.Load(ctx, meta.Name, meta.Fingerprint)
		if err != nil {
			log.Fatalf("load instructions skill=%s: %v", meta.Name, err)
		}
		if loaded.Instructions == "" {
			log.Fatalf("empty instructions skill=%s", meta.Name)
		}
		hits, err := catalog.Search(ctx, meta.Name, 5)
		if err != nil {
			log.Fatalf("search skill=%s: %v", meta.Name, err)
		}
		if len(hits) == 0 || hits[0].Name != meta.Name {
			log.Fatalf("exact-name retrieval failed skill=%s", meta.Name)
		}
		fmt.Printf("PASS %s: load, fingerprint, exact-name search\n", meta.Name)
	}
	fmt.Printf("PASS runtime catalog: %d skills, generation=%d\n", len(metadata), report.Generation)
	file, err := os.Open(filepath.Join(os.Args[1], "..", "evals", "cases.jsonl"))
	if err != nil {
		log.Fatalf("open search fixtures: %v", err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	total, found := 0, 0
	for scanner.Scan() {
		var row struct {
			ID    string `json:"id"`
			Query string `json:"query"`
			Skill string `json:"skill"`
		}
		if err := json.Unmarshal(scanner.Bytes(), &row); err != nil {
			log.Fatalf("parse search fixture: %v", err)
		}
		hits, err := catalog.Search(ctx, row.Query, 5)
		if err != nil {
			log.Fatalf("search fixture=%s: %v", row.ID, err)
		}
		total++
		matched := false
		for _, hit := range hits {
			if hit.Name == row.Skill {
				matched = true
				break
			}
		}
		if matched {
			found++
		} else {
			fmt.Printf("MISS candidate recall: %s query=%s\n", row.ID, row.Query)
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatalf("read search fixtures: %v", err)
	}
	fmt.Printf("Candidate recall@5: %d/%d (retrieval only, not model routing)\n", found, total)
	if found != total {
		log.Fatal("candidate recall fixture failures")
	}
}
