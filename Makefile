.PHONY: clone help

help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1

clone:
	Shell gemini "clone memorilabs/memori" \
		-d \
		--output-format json \
		--yolo
