# SmartBank Financial BI & Reporting Dashboard
## QA Test Strategy

**Document ID:** SB-BI-TS-001
**Version:** 1.0
**Status:** Draft

---

## 1. Purpose

Define the testing approach for the SmartBank Financial BI & Reporting
Dashboard. The strategy covers data correctness, business calculations,
API behavior, dashboard functionality, and automated regression.

## 2. Quality Objectives

- Verify that dashboard metrics comply with approved business rules.
- Verify that charts and tables represent the correct filtered dataset.
- Detect missing, duplicated, invalid, and inconsistent data.
- Verify consistent results across SQL, API, and dashboard layers.
- Validate date ranges, percentages, aggregation, and rounding.
- Automate repeatable regression scenarios.
- Produce reviewable test results through CI/CD.

## 3. Test Scope

### 3.1 Data and Database Testing

Validate:

- Required fields and data types.
- Primary and foreign key relationships where applicable.
- Duplicate and missing records.
- Valid transaction types, statuses, dates, and amounts.
- SQL totals, averages, counts, minimums, maximums, and grouped results.
- Date-boundary handling and filter criteria.
- Data reconciliation against independently calculated expected results.

### 3.2 API Testing

Validate:

- Response status codes and response structure.
- Required fields, data types, and null handling.
- KPI and chart data for supported filters.
- Date-range and combined-filter behavior.
- Empty results and invalid input handling.
- Agreement between API results and database calculations.

### 3.3 Dashboard UI Testing

Validate:

- KPI visibility and displayed values.
- Chart titles, categories, labels, and represented values.
- Date-range selection and category filters.
- Combined filters and reset behavior.
- Table contents, sorting, and pagination.
- Loading, error, and empty-result states.
- Consistency between the displayed data and independently verified results.

### 3.4 End-to-End Reconciliation

For selected scenarios, compare independently calculated expected results
against the database query, API response, and dashboard display.

All layers must use equivalent business rules, filters, date boundaries,
and rounding conventions.

## 4. Core Metrics and Calculation Checks

The test suite shall cover the following, as applicable:

- Total amount and transaction count.
- Average amount and qualifying record count.
- Minimum and maximum values.
- Category distribution and percentage totals.
- Percentage change against a defined, valid baseline.
- Daily, monthly, and selected-period aggregation.
- Empty datasets, zero denominators, negative values, and null values.
- Duplicate records and records at date-range boundaries.

Expected results shall be independently calculated and documented.
Tests shall not rely solely on hardcoded values returned by the UI itself.

## 5. Date-Range Testing

The dashboard is expected to support 1D, 5D, 1M, 6M, 1Y, and YTD selections.

Before finalizing date-related assertions, document:

- Calendar-day versus business-day behavior.
- Inclusive and exclusive date boundaries.
- Timezone and timestamp handling.
- YTD start and selected end date.
- Behavior when no records exist within the selected period.

Boundary tests shall verify records immediately before, at, and after applicable
date boundaries.

## 6. Test Design Techniques

Use:

- Positive and negative testing.
- Boundary-value analysis.
- Equivalence partitioning.
- Data-driven and parameterized testing.
- Filter-combination testing.
- Independent calculation and reconciliation.
- Regression testing.
- Exploratory testing for chart interactions and usability.

## 7. Automation Approach

- **SQL:** Independently validate database values and aggregations.
- **Python:** Calculate expected results and compare datasets.
- **Pandas:** Support structured data validation and reconciliation where useful.
- **API tests:** Validate service responses and filtering behavior.
- **Playwright for Python:** Automate browser interactions and visible results.
- **pytest:** Organize test cases, fixtures, parameterization, and assertions.
- **GitHub Actions:** Run approved automated tests and publish test artifacts.
- **Docker:** Support reproducible test execution.
- **Kubernetes:** Demonstrate container orchestration and test execution where appropriate.

The implementation shall use the existing project structure where practical
and preserve current SmartBank functionality.

## 8. Test Data Management

Use synthetic, controlled, and repeatable datasets.

Include scenarios for:

- Multiple account and transaction categories.
- Different transaction statuses.
- Multiple dates and reporting periods.
- Zero and negative values where valid for the metric.
- Null and missing values where permitted by the data contract.
- Duplicate and invalid records for data-quality testing.
- Empty result sets and filter combinations.

Document the expected result for each controlled dataset used in assertions.

## 9. Defect Management

Each confirmed defect should record:

- Defect ID and summary.
- Requirement and test scenario.
- Preconditions and test data.
- Steps to reproduce.
- Expected and actual results.
- Evidence, logs, or relevant query output.
- Severity, priority, and resolution status.

## 10. Entry Criteria

- Relevant requirements and acceptance criteria are reviewed.
- Required test data and expected calculations are available.
- The target application, API, or database is accessible.
- Dependencies and environment configuration are documented.

## 11. Exit Criteria

- Planned tests have been executed.
- Results and unresolved defects are documented.
- Critical business calculations and reconciliation scenarios pass, or exceptions
  have been explicitly reviewed and accepted.
- Regression tests pass for the scope being released.
- Test evidence and documentation are available for review.

## 12. Risks and Controls

| Risk | Control |
|---|---|
| Incorrect business definitions | Agree on metric formulas before asserting results |
| Date-boundary inconsistencies | Specify timezone and date-range rules |
| False confidence from UI-only tests | Reconcile against independent SQL and API results |
| Unstable chart selectors | Prefer accessible labels and deterministic test attributes |
| Unreliable test data | Use controlled synthetic datasets |
| Existing functionality regression | Run relevant SmartBank regression tests |
| Accidental unrelated commits | Review the Git diff and stage only approved files |

## 13. Related Artifacts

- BI Reporting Requirements
- BI Reporting Sprint Plan
- Metric and data definitions
- Requirements traceability matrix
- SQL validation scripts
- API, database, and UI automation tests
- Test execution reports

## 14. Change History

| Version | Description |
|---|---|
| 1.0 | Initial BI reporting QA test strategy |
