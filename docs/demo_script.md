# Demo Script

## 1. Problem

Architecture diagrams often exist before security review. Manual STRIDE modeling is useful but slow during hackathons and early design reviews.

## 2. Solution

ThreatGraph AI detects architecture components from an image, normalizes the topology, and uses specialized agents to generate a STRIDE report.

## 3. Flow

1. Upload a sample architecture image.
2. Review detected components and confidence levels.
3. Run analysis.
4. Show generated threats, vulnerabilities, countermeasures, and report.

## 4. Differentiator

The MVP includes a supervised detector and does not rely only on visual LLM interpretation.
