"""Registry of plan sections and metadata for UI rendering."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from django.db import models

from . import models as plan_models


@dataclass(frozen=True)
class TableConfig:
    key: str
    model: type[plan_models.BaseSection]
    title: str
    singleton: bool = False
    default_rows: List[dict[str, str]] = field(default_factory=list)

    @property
    def fields(self) -> list[str]:
        return [
            f.name
            for f in self.model._meta.fields
            if f.name not in {"id", "project", "created_at", "updated_at"}
        ]


@dataclass(frozen=True)
class SectionConfig:
    key: str
    title: str
    description: str
    tables: tuple[TableConfig, ...]


SINGLETON_MODELS: set[type[plan_models.BaseSection]] = {
    plan_models.ReferenceToPIF,
    plan_models.ReferenceToOtherDocuments,
    plan_models.PlanForOtherResource,
    plan_models.ReferenceToPIS,
    plan_models.ProductOverview,
    plan_models.LifeCycleModel,
    plan_models.OrganizationStructure,
    plan_models.SummaryEstimatesAssumptions,
    plan_models.TransitionPlan,
    plan_models.SupplierEvaluationCapability,
    plan_models.CyberSecurityAssessmentAndRelease,
    plan_models.ConfigurationManagementTools,
    plan_models.LocationOfCI,
    plan_models.Versioning,
    plan_models.Baselining,
    plan_models.ChangeManagementPlan,
    plan_models.BackupAndRetrieval,
    plan_models.Recovery,
    plan_models.ReleaseMechanism,
    plan_models.InformationRetentionPlan,
    plan_models.SupplierProjectIntroductionScope,
    plan_models.SupportProjectPlan,
    plan_models.SupplierConfigurationManagementPlan,
    plan_models.SAMLocationOfCI,
    plan_models.SAMVersioning,
    plan_models.SAMBaselining,
    plan_models.SAMChangeManagementPlan,
    plan_models.SAMConfigurationManagementAudit,
    plan_models.SAMBackup,
    plan_models.SAMReleaseMechanism,
    plan_models.SAMInformationRetentionPlan,
    plan_models.CyberSecurityRequirementsDesignModel,
    plan_models.CybersecurityCase,
    plan_models.FunctionalSafetyPlan,
    plan_models.OrganizationStructure,
}


def _table(key: str, model: type[plan_models.BaseSection], title: str, *, default_rows: Iterable[dict[str, str]] | None = None) -> TableConfig:
    return TableConfig(
        key=key,
        model=model,
        title=title,
        singleton=model in SINGLETON_MODELS,
        default_rows=list(default_rows or []),
    )


SECTIONS: tuple[SectionConfig, ...] = (
    SectionConfig(
        key="m1",
        title="M1 — Revision History",
        description="Track revisions and approvals for the project plan.",
        tables=(
            _table("revision-history", plan_models.RevisionHistory, "Revision History"),
        ),
    ),
    SectionConfig(
        key="m2",
        title="M2 — Table of Contents",
        description="Provide navigation links for the plan sections.",
        tables=(
            _table("toc", plan_models.TOCEntry, "Table of Contents"),
        ),
    ),
    SectionConfig(
        key="m3",
        title="M3 — Definitions & References",
        description="Maintain references and terminology used within the plan.",
        tables=(
            _table("definitions", plan_models.DefinitionAcronym, "Definitions & Acronyms"),
            _table("reference-pif", plan_models.ReferenceToPIF, "Reference To PIF"),
            _table("reference-other-docs", plan_models.ReferenceToOtherDocuments, "Reference To Other Documents"),
            _table("plan-other-resource", plan_models.PlanForOtherResource, "Plan For Other Resource"),
        ),
    ),
    SectionConfig(
        key="m4",
        title="M4 — Project Overview & Requirements",
        description="Capture project overview, lifecycle, assumptions and security needs.",
        tables=(
            _table("reference-pis", plan_models.ReferenceToPIS, "Reference To PIS"),
            _table("product-overview", plan_models.ProductOverview, "Product Overview"),
            _table("project-details", plan_models.ProjectDetails, "Project Details"),
            _table("lifecycle-model", plan_models.LifeCycleModel, "Lifecycle Model"),
            _table("assumptions", plan_models.Assumptions, "Assumptions"),
            _table("constraints", plan_models.Constraints, "Constraints"),
            _table("dependencies", plan_models.Dependencies, "Dependencies"),
            _table("business-continuity", plan_models.BusinessContinuity, "Business Continuity"),
            _table("cyber-security-design", plan_models.CyberSecurityRequirementsDesignModel, "Cyber Security Requirements Design Model"),
            _table("cybersecurity-case", plan_models.CybersecurityCase, "Cybersecurity Case"),
            _table("functional-safety-plan", plan_models.FunctionalSafetyPlan, "Functional Safety Plan"),
            _table("information-security-requirements", plan_models.InformationSecurityRequirements, "Information Security Requirements"),
        ),
    ),
    SectionConfig(
        key="m5",
        title="M5 — Resources & Planning",
        description="Outline stakeholders, resources, tools and reuse planning.",
        tables=(
            _table("organization-structure", plan_models.OrganizationStructure, "Organization Structure"),
            _table("stakeholders", plan_models.Stakeholder, "Stakeholders"),
            _table("human-resources", plan_models.HumanResourceAndSpecialTrainingPlan, "Human Resource & Training Plan"),
            _table("environment-tools", plan_models.EnvironmentAndTools, "Environment & Tools"),
            _table("build-buy-reuse", plan_models.BuildBuyReuse, "Build/Buy/Reuse"),
            _table("reuse-analysis", plan_models.ReuseAnalysis, "Reuse Analysis"),
            _table("summary-estimates", plan_models.SummaryEstimatesAssumptions, "Summary Estimates & Assumptions"),
            _table("size-complexity", plan_models.SizeAndComplexity, "Size & Complexity"),
            _table("duration-effort", plan_models.DurationEffortEstimateOrganizationNorms, "Duration & Effort Estimates"),
            _table("off-the-shelf", plan_models.UsageOfOffTheShelfComponent, "Usage of Off-the-shelf Components"),
            _table("cybersecurity-interface", plan_models.CybersecurityInterfaceAgreement, "Cybersecurity Interface Agreement"),
        ),
    ),
    SectionConfig(
        key="m6",
        title="M6 — Monitoring & Control",
        description="Define monitoring cadence and quantitative objectives.",
        tables=(
            _table("monitoring-control", plan_models.ProjectMonitoringAndControl, "Project Monitoring & Control"),
            _table("quantitative-objectives", plan_models.QuantitativeObjectivesMeasurementAndDataManagementPlan, "Quantitative Objectives"),
            _table("transition-plan", plan_models.TransitionPlan, "Transition Plan"),
        ),
    ),
    SectionConfig(
        key="m7",
        title="M7 — Quality Management",
        description="Maintain quality standards, verification, and causal analysis plans.",
        tables=(
            _table("standards-qm", plan_models.StandardsQM, "Standards"),
            _table("verification-validation", plan_models.VerificationAndValidationPlan, "Verification & Validation Plan"),
            _table("confirmation-review", plan_models.ConfirmationReviewPlan, "Confirmation Review Plan"),
            _table("proactive-causal", plan_models.ProactiveCausalAnalysisPlan, "Proactive Causal Analysis"),
            _table("reactive-causal", plan_models.ReactiveCausalAnalysisPlan, "Reactive Causal Analysis"),
            _table("supplier-evaluation", plan_models.SupplierEvaluationCapability, "Supplier Evaluation Capability"),
            _table("cybersecurity-assessment", plan_models.CyberSecurityAssessmentAndRelease, "Cyber Security Assessment & Release"),
        ),
    ),
    SectionConfig(
        key="m8",
        title="M8 — Decision Management & Release",
        description="Capture decisions, tailoring and release plans.",
        tables=(
            _table("decision-management", plan_models.DecisionManagementPlan, "Decision Management Plan"),
            _table("tailoring-qms", plan_models.TailoringQMS, "Tailoring QMS"),
            _table("deviations", plan_models.Deviations, "Deviations"),
            _table("product-release", plan_models.ProductReleasePlan, "Product Release Plan"),
            _table("tailoring-component", plan_models.TailoringDueToComponentOutOfContext, "Tailoring Due To Component Out Of Context"),
            _table("release-cybersecurity-interface", plan_models.ReleaseCybersecurityInterfaceAgreement, "Release Cybersecurity Interface Agreement"),
        ),
    ),
    SectionConfig(
        key="m9",
        title="M9 — Risk Management",
        description="Manage risks, mitigations and exposure history.",
        tables=(
            _table("risk-management-plan", plan_models.RiskManagementPlan, "Risk Management Plan"),
            _table("risk-mitigation", plan_models.RiskMitigationAndContingency, "Risk Mitigation & Contingency"),
        ),
    ),
    SectionConfig(
        key="m10",
        title="M10 — Opportunity Management",
        description="Track opportunities and their evolution.",
        tables=(
            _table("opportunity-register", plan_models.OpportunityRegister, "Opportunity Register"),
            _table("opportunity-plan", plan_models.OpportunityManagementPlan, "Opportunity Management Plan"),
        ),
    ),
    SectionConfig(
        key="m11",
        title="M11 — Configuration Management",
        description="Define configuration management strategy and responsibilities.",
        tables=(
            _table("configuration-tools", plan_models.ConfigurationManagementTools, "Configuration Management Tools"),
            _table("configuration-items", plan_models.ListOfConfigurationItems, "Configuration Items"),
            _table("non-configuration-items", plan_models.ListOfNonConfigurableItems, "Non-Configurable Items"),
            _table("naming-convention", plan_models.NamingConvention, "Naming Convention"),
            _table("location-ci", plan_models.LocationOfCI, "Location Of CI"),
            _table("versioning", plan_models.Versioning, "Versioning"),
            _table("baselining", plan_models.Baselining, "Baselining"),
            _table("branching-merging", plan_models.BranchingAndMerging, "Branching & Merging"),
            _table("labelling-baselines", plan_models.LabellingBaselines, "Labelling Baselines"),
            _table("labelling-baselines2", plan_models.LabellingBaselines2, "Labelling Baselines (Branch Tags)"),
            _table("change-management", plan_models.ChangeManagementPlan, "Change Management Plan"),
            _table("configuration-control", plan_models.ConfigurationControl, "Configuration Control"),
            _table("configuration-control-board", plan_models.ConfigurationControlBoard, "Configuration Control Board"),
            _table("configuration-status", plan_models.ConfigurationStatusAccounting, "Configuration Status Accounting"),
            _table("configuration-audit", plan_models.ConfigurationManagementAudit, "Configuration Management Audit"),
            _table("backup-retrieval", plan_models.BackupAndRetrieval, "Backup & Retrieval"),
            _table("recovery", plan_models.Recovery, "Recovery"),
            _table("release-mechanism", plan_models.ReleaseMechanism, "Release Mechanism"),
            _table("information-retention", plan_models.InformationRetentionPlan, "Information Retention Plan"),
        ),
    ),
    SectionConfig(
        key="m12",
        title="M12 — Deliverables",
        description="Monitor planned deliverables and milestones.",
        tables=(
            _table(
                "deliverables",
                plan_models.DeliverableMilestone,
                "Deliverables",
                default_rows=[
                    {"work_product": name, "sl_no": str(idx + 1)}
                    for idx, name in enumerate(
                        [
                            "Statement of Work",
                            "Project Plan",
                            "Estimation",
                            "Requirements document",
                            "Design document",
                            "Coding Guidelines",
                            "Source Code",
                            "Executables",
                            "Release Notes",
                            "Test Design and Report",
                            "Review Form and Report",
                            "User Manual",
                            "Installation Manual",
                            "Project Metrics Report",
                            "Casual Analysis and Resolution",
                        ]
                    )
                ],
            ),
        ),
    ),
    SectionConfig(
        key="m13",
        title="M13 — Supplier Agreement Management",
        description="Coordinate supplier scope, risks and deliverables.",
        tables=(
            _table("supplier-intro", plan_models.SupplierProjectIntroductionScope, "Supplier Project Introduction & Scope"),
            _table("support-plan", plan_models.SupportProjectPlan, "Support Project Plan"),
            _table("sam-assumptions", plan_models.SAMAssumptions, "SAM Assumptions"),
            _table("sam-constraints", plan_models.SAMConstraints, "SAM Constraints"),
            _table("sam-dependencies", plan_models.SAMDependencies, "SAM Dependencies"),
            _table("sam-risks", plan_models.SAMRisks, "SAM Risks"),
            _table(
            "sam-status",
            plan_models.SAMStatusReportingAndCommunicationPlan,
            "SAM Status Reporting & Communication",
            default_rows=[
                {"type_of_progress_reviews": value, "sl_no": str(idx + 1)}
                for idx, value in enumerate(
                    [
                        "Internal Team reviews",
                        "Metrics reporting",
                        "Process compliance index audits",
                        "Supplier audits",
                        "Management Review",
                        "Others (specify)",
                    ]
                )
            ],
        ),
            _table("sam-quantitative", plan_models.SAMQuantitativeObjectivesMeasurementAndDataManagementPlan, "SAM Quantitative Objectives"),
            _table("sam-verification", plan_models.SAMVerificationAndValidationPlan, "SAM Verification & Validation"),
            _table("supplier-config-plan", plan_models.SupplierConfigurationManagementPlan, "Supplier Configuration Management Plan"),
            _table("tailoring-sam", plan_models.TailoringSAM, "Tailoring SAM"),
            _table("sam-deviations", plan_models.SAMDeviations, "SAM Deviations"),
            _table("sam-product-release", plan_models.SAMProductReleasePlan, "SAM Product Release Plan"),
            _table("sam-location-ci", plan_models.SAMLocationOfCI, "SAM Location Of CI"),
            _table("sam-versioning", plan_models.SAMVersioning, "SAM Versioning"),
            _table("sam-baselining", plan_models.SAMBaselining, "SAM Baselining"),
            _table("sam-labelling", plan_models.SAMLabellingBaselines, "SAM Labelling Baselines"),
            _table("sam-labelling2", plan_models.SAMLabellingBaselines2, "SAM Labelling Baselines (Branch Tags)"),
            _table("sam-change-management", plan_models.SAMChangeManagementPlan, "SAM Change Management Plan"),
            _table("sam-configuration-control", plan_models.SAMConfigurationControl, "SAM Configuration Control"),
            _table("sam-configuration-audit", plan_models.SAMConfigurationManagementAudit, "SAM Configuration Management Audit"),
            _table("sam-backup", plan_models.SAMBackup, "SAM Backup"),
            _table("sam-release-mechanism", plan_models.SAMReleaseMechanism, "SAM Release Mechanism"),
            _table("sam-information-retention", plan_models.SAMInformationRetentionPlan, "SAM Information Retention Plan"),
            _table(
                "sam-deliverables",
                plan_models.SAMDeliverableMilestone,
                "SAM Deliverables",
                default_rows=[
                    {"work_product": name, "sl_no": str(idx + 1)}
                    for idx, name in enumerate(
                        [
                            "Statement of Work",
                            "Project Plan",
                            "Estimation",
                            "Requirements document",
                            "Design document",
                            "Coding Guidelines",
                            "Source Code",
                            "Executables",
                            "Release Notes",
                            "Test Design and Report",
                            "Review Form and Report",
                            "User Manual",
                            "Installation Manual",
                            "Project Metrics Report",
                            "Casual Analysis and Resolution",
                        ]
                    )
                ],
            ),
        ),
    ),
)


def get_section_by_key(key: str) -> SectionConfig | None:
    for section in SECTIONS:
        if section.key == key:
            return section
    return None


def find_table_config(table_key: str) -> TableConfig | None:
    for section in SECTIONS:
        for table in section.tables:
            if table.key == table_key:
                return table
    return None
