"""Data models for project plan templates."""
from __future__ import annotations

from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - helper
        return self.name


class ProjectMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project", "user")
        verbose_name = "Project membership"
        verbose_name_plural = "Project memberships"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user} -> {self.project} ({'Editor' if self.can_edit else 'Viewer'})"


class BaseSection(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["pk"]


# M1 Section - Revision History
class RevisionHistory(BaseSection):
    revision_no = models.CharField(max_length=50)
    change_description = models.TextField()
    reviewed_by = models.CharField(max_length=255, blank=True)
    approved_by = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    remarks = models.TextField(blank=True)


# M2 Section - TOC
class TOCEntry(BaseSection):
    sheet_name = models.CharField(max_length=255)
    sections_in_sheet = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)


# M3 Section - Definitions, References
class DefinitionAcronym(BaseSection):
    term = models.CharField(max_length=255)
    definition = models.TextField()


class ReferenceToPIF(BaseSection):
    content = models.TextField()


class ReferenceToOtherDocuments(BaseSection):
    content = models.TextField()


class PlanForOtherResource(BaseSection):
    content = models.TextField()


# M4 Section - Project Overview & Requirements
class ReferenceToPIS(BaseSection):
    content = models.TextField()


class ProductOverview(BaseSection):
    content = models.TextField()


class ProjectDetails(BaseSection):
    project_model = models.CharField(max_length=255)
    project_type = models.CharField(max_length=255)
    software_type = models.CharField(max_length=255, blank=True)
    standard_to_be_followed = models.CharField(max_length=255, blank=True)
    customer = models.CharField(max_length=255, blank=True)
    programming_language = models.CharField(max_length=255, blank=True)
    project_duration = models.CharField(max_length=255, blank=True)
    team_size = models.CharField(max_length=255, blank=True)


class LifeCycleModel(BaseSection):
    content = models.TextField()
    image_input = models.FileField(upload_to="lifecycle_models/", blank=True, null=True)


class Assumptions(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_on_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class Constraints(BaseSection):
    constraint_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_on_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class Dependencies(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_on_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class BusinessContinuity(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_of_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class CyberSecurityRequirementsDesignModel(BaseSection):
    content = models.TextField()


class CybersecurityCase(BaseSection):
    content = models.TextField()


class FunctionalSafetyPlan(BaseSection):
    content = models.TextField()


class InformationSecurityRequirements(BaseSection):
    sl_no = models.PositiveIntegerField()
    phase = models.CharField(max_length=255)
    is_requirement_description = models.TextField()
    monitoring_control = models.TextField(blank=True)
    tools = models.CharField(max_length=255, blank=True)
    artifacts = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


# M5 Section - Resources & Planning
class OrganizationStructure(BaseSection):
    content = models.TextField()
    image_input = models.FileField(upload_to="org_structures/", blank=True, null=True)


class Stakeholder(BaseSection):
    sl_no = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    stakeholder_type = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    authority_responsibility = models.TextField(blank=True)
    contact_details = models.CharField(max_length=255, blank=True)


class HumanResourceAndSpecialTrainingPlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    role = models.CharField(max_length=255)
    skill_experience_required = models.TextField()
    no_of_people_required = models.PositiveIntegerField()
    available = models.PositiveIntegerField(default=0)
    project_specific_training_needs = models.TextField(blank=True)


class EnvironmentAndTools(BaseSection):
    sl_no = models.PositiveIntegerField()
    name_brief_description = models.CharField(max_length=255)
    no_of_licenses_required = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class BuildBuyReuse(BaseSection):
    sl_no = models.PositiveIntegerField()
    component_product = models.CharField(max_length=255)
    build_buy_reuse = models.CharField(max_length=255)
    reuse_goals_objectives = models.TextField(blank=True)
    vendor_project_name_version = models.CharField(max_length=255, blank=True)
    responsible_person_reuse = models.CharField(max_length=255, blank=True)
    quality_evaluation_criteria = models.TextField(blank=True)
    responsible_person_qualification = models.CharField(max_length=255, blank=True)
    modifications_planned = models.TextField(blank=True)
    selected_item_operational_environment = models.TextField(blank=True)
    known_defect_vulnerabilities_limitations = models.TextField(blank=True)


class ReuseAnalysis(BaseSection):
    sl_no = models.PositiveIntegerField()
    component_product = models.CharField(max_length=255)
    reuse = models.CharField(max_length=255)
    modifications_required = models.TextField(blank=True)
    constraints_for_reuse = models.TextField(blank=True)
    risk_analysis_result = models.TextField(blank=True)
    impact_on_plan_activities = models.TextField(blank=True)
    evaluation_to_comply_cyber_security = models.TextField(blank=True)
    impact_on_integration_documents = models.TextField(blank=True)
    known_defects = models.TextField(blank=True)


class SummaryEstimatesAssumptions(BaseSection):
    content = models.TextField()


class SizeAndComplexity(BaseSection):
    sl_no = models.PositiveIntegerField()
    product_component_module = models.CharField(max_length=255)
    size_kloc = models.CharField(max_length=255, blank=True)
    percent_reuse_estimated = models.CharField(max_length=255, blank=True)
    effort_person_days_weeks_months = models.CharField(max_length=255, blank=True)
    complexity = models.CharField(max_length=255, blank=True)


class DurationEffortEstimateOrganizationNorms(BaseSection):
    phase_milestone = models.CharField(max_length=255)
    schedule_days_weeks = models.CharField(max_length=255, blank=True)
    effort_person_days_weeks = models.CharField(max_length=255, blank=True)
    remarks_on_deviation = models.TextField(blank=True)


class UsageOfOffTheShelfComponent(BaseSection):
    sl_no = models.PositiveIntegerField()
    name_of_component = models.CharField(max_length=255)
    requirements_complied = models.CharField(max_length=255, blank=True)
    requirement_document_updated = models.CharField(max_length=255, blank=True)
    specific_application_context = models.TextField(blank=True)
    documentation_sufficient = models.CharField(max_length=255, blank=True)
    vulnerabilities_identified = models.CharField(max_length=255, blank=True)
    integration_document_updated = models.CharField(max_length=255, blank=True)
    test_design_document = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class CybersecurityInterfaceAgreement(BaseSection):
    sl_no = models.PositiveIntegerField()
    phase = models.CharField(max_length=255)
    work_product = models.CharField(max_length=255)
    document_ref = models.CharField(max_length=255, blank=True)
    supplier = models.CharField(max_length=255, blank=True)
    customer = models.CharField(max_length=255, blank=True)
    level_of_confidentiality = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


# M6 Section - Monitoring & Control
class ProjectMonitoringAndControl(BaseSection):
    sl_no = models.PositiveIntegerField()
    type_of_progress_reviews = models.CharField(max_length=255)
    month_phase_milestone_frequency = models.CharField(max_length=255, blank=True)
    participants = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)
    mode_of_communication = models.CharField(max_length=255, blank=True)


class QuantitativeObjectivesMeasurementAndDataManagementPlan(BaseSection):
    objective = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    priority = models.CharField(max_length=255, blank=True)
    project_goal = models.CharField(max_length=255, blank=True)
    organisation_norm = models.CharField(max_length=255, blank=True)
    data_source = models.CharField(max_length=255, blank=True)
    reason_for_deviation_from_organization_norm = models.TextField(blank=True)


class TransitionPlan(BaseSection):
    content = models.TextField()


# M7 Section - Quality Management
class StandardsQM(BaseSection):
    sl_no = models.PositiveIntegerField()
    name_of_standard = models.CharField(max_length=255)
    brief_description = models.TextField(blank=True)
    source = models.CharField(max_length=255, blank=True)


class VerificationAndValidationPlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    artifact_name = models.CharField(max_length=255)
    verification_method = models.CharField(max_length=255, blank=True)
    verification_type = models.CharField(max_length=255, blank=True)
    validation_method = models.CharField(max_length=255, blank=True)
    validation_type = models.CharField(max_length=255, blank=True)
    tools_used = models.CharField(max_length=255, blank=True)
    approving_authority = models.CharField(max_length=255, blank=True)
    verification_validation_evidence = models.TextField(blank=True)
    remarks_deviation = models.TextField(blank=True)


class ConfirmationReviewPlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    artifact_name = models.CharField(max_length=255)
    phase = models.CharField(max_length=255)
    confirmation_measure = models.CharField(max_length=255)
    plan_schedule = models.CharField(max_length=255, blank=True)
    asil = models.CharField(max_length=255, blank=True)
    independence_level = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class ProactiveCausalAnalysisPlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    previous_similar_projects_executed = models.TextField(blank=True)
    major_issues_defects_identified_by_customer = models.TextField(blank=True)
    corrective_preventive_measures = models.TextField(blank=True)


class ReactiveCausalAnalysisPlan(BaseSection):
    Sl_No = models.PositiveIntegerField()
    Phase_Milestone = models.CharField(max_length=255)
    Brief_description_of_instances_when_causal_analysis_needs_to_be_done = models.TextField(blank=True)
    Causal_Analysis_Method_Tool = models.CharField(max_length=255, blank=True)
    Responsibility = models.CharField(max_length=255, blank=True)


class SupplierEvaluationCapability(BaseSection):
    content = models.TextField()


class CyberSecurityAssessmentAndRelease(BaseSection):
    content = models.TextField()


# M8 Section - Decision Management & Release
class DecisionManagementPlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    phase_milestone = models.CharField(max_length=255)
    brief_description_of_major_decisions = models.TextField()
    decision_making_method_tool = models.CharField(max_length=255, blank=True)
    responsibility = models.CharField(max_length=255, blank=True)


class TailoringQMS(BaseSection):
    Sl_No = models.PositiveIntegerField()
    Brief_description_of_Deviation = models.TextField()
    Reasons_Justifications = models.TextField(blank=True)
    Remarks = models.TextField(blank=True)


class Deviations(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description_of_deviation = models.TextField()
    reasons_justifications = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class ProductReleasePlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    release_type = models.CharField(max_length=255)
    objective = models.TextField(blank=True)
    release_date_milestones = models.CharField(max_length=255, blank=True)
    mode_of_delivery = models.CharField(max_length=255, blank=True)
    qa_release_audit_date = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class TailoringDueToComponentOutOfContext(BaseSection):
    sl_no = models.PositiveIntegerField()
    name_of_the_out_of_context_component = models.CharField(max_length=255)
    name_of_the_cyber_security_requirements_impacted = models.TextField(blank=True)
    external_interfaces_document = models.CharField(max_length=255, blank=True)
    impact_on_cyber_security_claims = models.TextField(blank=True)
    impact_on_cyber_security_assumptions = models.TextField(blank=True)
    validations_of_requirement_assumption_and_claims_are_done = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class ReleaseCybersecurityInterfaceAgreement(BaseSection):
    sl_no = models.PositiveIntegerField()
    phase = models.CharField(max_length=255)
    work_product = models.CharField(max_length=255)
    document_ref = models.CharField(max_length=255, blank=True)
    supplier_r_a_s_i_c = models.CharField(max_length=255, blank=True)
    customer_r_a_s_i_c = models.CharField(max_length=255, blank=True)
    level_of_confidentiality = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


# M9 Section - Risk Management
class RiskManagementPlan(BaseSection):
    risk_identification_method = models.TextField()
    phase_sprint_milestone = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class RiskMitigationAndContingency(BaseSection):
    RiskId = models.CharField(max_length=255)
    RiskDescription = models.TextField()
    RiskCategory = models.CharField(max_length=255, blank=True)
    RiskOriginatorName = models.CharField(max_length=255, blank=True)
    RiskSource = models.CharField(max_length=255, blank=True)
    DateOfRiskIdentification = models.DateField()
    PhaseOfRiskIdentification = models.CharField(max_length=255, blank=True)
    RiskTreatmentOption = models.CharField(max_length=255, blank=True)
    RationaleToChooseRiskTreatmentOption = models.TextField(blank=True)
    EffortRequiredForRiskTreatment = models.CharField(max_length=255, blank=True)
    RiskTreatmentSchedule = models.CharField(max_length=255, blank=True)
    SuccessCriteriaForRiskTreatmentActivities = models.TextField(blank=True)
    CriteriaForCancellationOfRiskTreatmentActivities = models.TextField(blank=True)
    FrequencyOfMonitoringRiskTreatmentActivities = models.CharField(max_length=255, blank=True)
    Threshold = models.CharField(max_length=255, blank=True)
    Trigger = models.CharField(max_length=255, blank=True)
    Probability = models.CharField(max_length=255, blank=True)
    Impact = models.CharField(max_length=255, blank=True)
    RiskExposure = models.CharField(max_length=255, blank=True)
    MitigationPlan = models.TextField(blank=True)
    ContingencyPlan = models.TextField(blank=True)
    VerificationMethodsForMitigationContingencyPlan = models.TextField(blank=True)
    ListOfStakeholders = models.TextField(blank=True)
    Responsibility = models.CharField(max_length=255, blank=True)
    Status = models.CharField(max_length=255, blank=True)
    Remarks = models.TextField(blank=True)


class RiskExposureHistory(models.Model):
    risk = models.ForeignKey(RiskMitigationAndContingency, on_delete=models.CASCADE, related_name="exposure_history")
    date = models.DateField()
    exposure_value = models.CharField(max_length=255)

    class Meta:
        ordering = ["-date"]


# M10 Section - Opportunity Management
class OpportunityRegister(BaseSection):
    Opportunity_Id = models.CharField(max_length=255)
    Opportunity_Description = models.TextField()
    Opportunity_Category = models.CharField(max_length=255, blank=True)
    Opportunity_Source = models.CharField(max_length=255, blank=True)
    Date_of_Identification = models.DateField()
    Phase_of_Identification = models.CharField(max_length=255, blank=True)
    Cost = models.CharField(max_length=255, blank=True)
    Benefit = models.CharField(max_length=255, blank=True)
    Opportunity_Value = models.CharField(max_length=255, blank=True)
    Leverage_Plan_to_maximize_Opportunities_identified = models.TextField(blank=True)
    Responsibility = models.CharField(max_length=255, blank=True)
    Status = models.CharField(max_length=255, blank=True)
    Remarks = models.TextField(blank=True)


class OpportunityManagementPlan(BaseSection):
    Sl_No = models.PositiveIntegerField()
    OpportunityIdentificationMethod = models.CharField(max_length=255)
    PhaseSprintMilestone = models.CharField(max_length=255, blank=True)
    Remarks = models.TextField(blank=True)


class OpportunityValueHistory(models.Model):
    opportunity = models.ForeignKey(OpportunityRegister, on_delete=models.CASCADE, related_name="value_history")
    date = models.DateField()
    opportunity_value = models.CharField(max_length=255)

    class Meta:
        ordering = ["-date"]


# M11 Section - Configuration Management
class ConfigurationManagementTools(BaseSection):
    content = models.TextField()


class ListOfConfigurationItems(BaseSection):
    sl_no = models.PositiveIntegerField()
    ci_name_description = models.CharField(max_length=255)
    source = models.CharField(max_length=255, blank=True)
    format_type = models.CharField(max_length=255, blank=True)
    description_of_level = models.TextField(blank=True)
    branching_merging_required = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class ListOfNonConfigurableItems(BaseSection):
    sl_no = models.PositiveIntegerField()
    ci_name_description = models.CharField(max_length=255)
    source = models.CharField(max_length=255, blank=True)
    format_type = models.CharField(max_length=255, blank=True)
    description_of_level = models.TextField(blank=True)
    branching_merging_required = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class NamingConvention(BaseSection):
    Sl_No = models.PositiveIntegerField()
    Files_and_Folders = models.CharField(max_length=255)
    Naming_Convention = models.CharField(max_length=255)
    Name_of_CI = models.CharField(max_length=255, blank=True)


class LocationOfCI(BaseSection):
    content = models.TextField()


class Versioning(BaseSection):
    content = models.TextField()


class Baselining(BaseSection):
    content = models.TextField()


class BranchingAndMerging(BaseSection):
    Sl_No = models.PositiveIntegerField()
    Branch_convention = models.CharField(max_length=255)
    Phase = models.CharField(max_length=255, blank=True)
    Branch_Name = models.CharField(max_length=255)
    Risk_associated_with_Branching = models.TextField(blank=True)
    Verification = models.CharField(max_length=255, blank=True)


class LabellingBaselines(BaseSection):
    sl_no = models.PositiveIntegerField()
    ci = models.CharField(max_length=255)
    planned_baseline_phase_milestone_date = models.CharField(max_length=255, blank=True)
    criteria_for_baseline = models.TextField(blank=True)
    baseline_name_label_or_tag = models.CharField(max_length=255, blank=True)


class LabellingBaselines2(BaseSection):
    sl_no = models.PositiveIntegerField()
    branch_convention = models.CharField(max_length=255)
    phase = models.CharField(max_length=255, blank=True)
    branch_name_tag = models.CharField(max_length=255)


class ChangeManagementPlan(BaseSection):
    content = models.TextField()


class ConfigurationControl(BaseSection):
    sl_no = models.PositiveIntegerField()
    ci_or_folder_name_path = models.CharField(max_length=255)
    developer_role = models.CharField(max_length=255, blank=True)
    team_leader_role = models.CharField(max_length=255, blank=True)
    em_role = models.CharField(max_length=255, blank=True)
    ed_role = models.CharField(max_length=255, blank=True)
    qa_role = models.CharField(max_length=255, blank=True)
    ccb_member = models.CharField(max_length=255, blank=True)


class ConfigurationControlBoard(BaseSection):
    sl_no = models.PositiveIntegerField()
    ccb_members_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    remarks_need_for_inclusion = models.TextField(blank=True)


class ConfigurationStatusAccounting(BaseSection):
    sl_no = models.PositiveIntegerField()
    phase_milestone_month = models.CharField(max_length=255)


class ConfigurationManagementAudit(BaseSection):
    sl_no = models.PositiveIntegerField()
    phase_milestone_month = models.CharField(max_length=255)


class BackupAndRetrieval(BaseSection):
    content = models.TextField()


class Recovery(BaseSection):
    content = models.TextField()


class ReleaseMechanism(BaseSection):
    content = models.TextField()


class InformationRetentionPlan(BaseSection):
    content = models.TextField()


# M12 Section - List Of Deliverables
class DeliverableMilestone(BaseSection):
    sl_no = models.PositiveIntegerField()
    work_product = models.CharField(max_length=255)
    owner_of_deliverable = models.CharField(max_length=255, blank=True)
    approving_authority = models.CharField(max_length=255, blank=True)
    release_to_customer = models.CharField(max_length=255, blank=True)
    milestone_a = models.CharField(max_length=255, blank=True)
    milestone_b = models.CharField(max_length=255, blank=True)
    milestone_c = models.CharField(max_length=255, blank=True)
    milestone_d = models.CharField(max_length=255, blank=True)


# M13 Section - Supplier Agreement Management
class SupplierProjectIntroductionScope(BaseSection):
    content = models.TextField()


class SupportProjectPlan(BaseSection):
    content = models.TextField()


class SAMAssumptions(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_on_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class SAMConstraints(BaseSection):
    constraint_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_on_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class SAMDependencies(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_on_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class SAMRisks(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description = models.TextField()
    impact_of_project_objectives = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class SAMStatusReportingAndCommunicationPlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    type_of_progress_reviews = models.CharField(max_length=255)
    month_phase_milestone_frequency = models.CharField(max_length=255, blank=True)
    participants = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class SAMQuantitativeObjectivesMeasurementAndDataManagementPlan(BaseSection):
    objective = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    project_goal = models.CharField(max_length=255, blank=True)
    organisation_norm = models.CharField(max_length=255, blank=True)
    data_source = models.CharField(max_length=255, blank=True)
    reason_for_deviation_from_organization_norm = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class SAMVerificationAndValidationPlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    work_product = models.CharField(max_length=255)
    verification_method = models.CharField(max_length=255, blank=True)
    validation_method = models.CharField(max_length=255, blank=True)
    approving_authority = models.CharField(max_length=255, blank=True)
    remarks_for_deviation = models.TextField(blank=True)


class SupplierConfigurationManagementPlan(BaseSection):
    content = models.TextField()


class TailoringSAM(BaseSection):
    Sl_No = models.PositiveIntegerField()
    Brief_description_of_Deviation = models.TextField()
    Reasons_Justifications = models.TextField(blank=True)
    Remarks = models.TextField(blank=True)


class SAMDeviations(BaseSection):
    sl_no = models.PositiveIntegerField()
    brief_description_of_deviation = models.TextField()
    reasons_justifications = models.TextField(blank=True)
    remarks = models.TextField(blank=True)


class SAMProductReleasePlan(BaseSection):
    sl_no = models.PositiveIntegerField()
    release_type = models.CharField(max_length=255)
    objective = models.TextField(blank=True)
    release_date_milestones = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)


class SAMLocationOfCI(BaseSection):
    content = models.TextField()


class SAMVersioning(BaseSection):
    content = models.TextField()


class SAMBaselining(BaseSection):
    content = models.TextField()


class SAMLabellingBaselines(BaseSection):
    sl_no = models.PositiveIntegerField()
    ci = models.CharField(max_length=255)
    planned_baseline_phase_milestone_date = models.CharField(max_length=255, blank=True)
    criteria_for_baseline = models.TextField(blank=True)
    baseline_name_label_or_tag = models.CharField(max_length=255, blank=True)


class SAMLabellingBaselines2(BaseSection):
    sl_no = models.PositiveIntegerField()
    branch_convention = models.CharField(max_length=255)
    phase = models.CharField(max_length=255, blank=True)
    branch_name_tag = models.CharField(max_length=255)


class SAMChangeManagementPlan(BaseSection):
    content = models.TextField()


class SAMConfigurationControl(BaseSection):
    sl_no = models.PositiveIntegerField()
    ci_or_folder_name_path = models.CharField(max_length=255)
    developer_role = models.CharField(max_length=255, blank=True)
    team_leader_role = models.CharField(max_length=255, blank=True)
    pm_role = models.CharField(max_length=255, blank=True)
    pgm_dh_role = models.CharField(max_length=255, blank=True)
    qa_role = models.CharField(max_length=255, blank=True)
    ccb_member = models.CharField(max_length=255, blank=True)


class SAMConfigurationManagementAudit(BaseSection):
    content = models.TextField()


class SAMBackup(BaseSection):
    content = models.TextField()


class SAMReleaseMechanism(BaseSection):
    content = models.TextField()


class SAMInformationRetentionPlan(BaseSection):
    content = models.TextField()


class SAMDeliverableMilestone(BaseSection):
    sl_no = models.PositiveIntegerField()
    work_product = models.CharField(max_length=255)
    owner_of_deliverable = models.CharField(max_length=255, blank=True)
    approving_authority = models.CharField(max_length=255, blank=True)
    release_to_tsbj = models.CharField(max_length=255, blank=True)
    milestone_a = models.CharField(max_length=255, blank=True)
    milestone_b = models.CharField(max_length=255, blank=True)
    milestone_c = models.CharField(max_length=255, blank=True)
    milestone_d = models.CharField(max_length=255, blank=True)
