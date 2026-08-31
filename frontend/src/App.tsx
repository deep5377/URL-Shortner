import { useEffect, useState } from "react";
import { api } from "./api";
import type { Metrics, Workflow } from "./types";
import { ApprovalGate } from "./components/ApprovalGate";
import { Dashboard } from "./components/Dashboard";
import { Metrics as MetricsView } from "./components/Metrics";
import { RequirementForm } from "./components/RequirementForm";
import { Sidebar } from "./components/Sidebar";
import { URLShortener } from "./components/URLShortener";
import { WorkflowDetail } from "./components/WorkflowDetail";
import { WorkflowList } from "./components/WorkflowList";

export default function App() {
	const [page, setPage] = useState("dashboard");
	const [workflow, setWorkflow] = useState<Workflow>();
	const [metrics, setMetrics] = useState<Metrics>();
	const [busy, setBusy] = useState(false);
	const [error, setError] = useState("");
	const [apiOnline, setApiOnline] = useState(false);
	const [workflows, setWorkflows] = useState<Workflow[]>([]);

	const refresh = async () => {
		try {
			await api.health();
			setApiOnline(true);
		} catch {
			setApiOnline(false);
			return;
		}
		try {
			setMetrics(await api.metrics());
			setWorkflows(await api.getWorkflows());
			if (workflow) setWorkflow(await api.getWorkflow(workflow.workflow_id));
		} catch { setError("The API is reachable, but workflow data could not be loaded."); }
	};

	useEffect(() => { void refresh(); }, [workflow?.workflow_id]);
	useEffect(() => {
		if (!workflow || !["RUNNING", "RETRY_REQUIRED"].includes(workflow.status)) return;
		const timer = window.setInterval(() => void refresh(), 1500);
		return () => window.clearInterval(timer);
	}, [workflow?.workflow_id, workflow?.status]);

	const start = async (requirement: string) => {
		setBusy(true);
		setError("");
		try {
			const next = await api.startWorkflow(requirement);
			setWorkflow(next);
			setPage("workflows");
			await refresh();
		} catch (err) {
			setError(err instanceof Error ? err.message : "Unable to start workflow. Verify that the backend is running.");
		} finally { setBusy(false); }
	};

	const clarify = async (value: string) => {
		if (!workflow) return;
		setBusy(true);
		try { setWorkflow(await api.clarify(workflow.workflow_id, value)); }
		catch (err) { setError(err instanceof Error ? err.message : "Unable to re-plan workflow."); }
		finally { setBusy(false); }
	};

	const approve = async (name: string) => {
		if (!workflow) return;
		setBusy(true);
		try { setWorkflow(await api.approve(workflow.workflow_id, name)); await refresh(); }
		catch (err) { setError(err instanceof Error ? err.message : "Unable to record approval."); }
		finally { setBusy(false); }
	};

	const reject = async (name: string, reason: string) => {
		if (!workflow) return;
		setBusy(true);
		try { setWorkflow(await api.reject(workflow.workflow_id, name, reason)); await refresh(); }
		catch (err) { setError(err instanceof Error ? err.message : "Unable to record rejection."); }
		finally { setBusy(false); }
	};

	return <div className="app-shell">
		<Sidebar active={page} onNavigate={setPage} />
		<main className="main">
			<header className="topbar">
				<button title="Open dashboard" aria-label="Open dashboard" className="mobile-brand" onClick={() => setPage("dashboard")}>✦ AGENTIC</button>
				<div className="breadcrumb">ENGINEERING CONTROL CENTER <span>/</span> {page.replace("-", " ")}</div>
				<div className={`top-status ${apiOnline ? "online" : "offline"}`}><i /> API {apiOnline ? "ONLINE" : "OFFLINE"}</div>
			</header>
			{error && <div className="global-error">{error}<button title="Dismiss error" aria-label="Dismiss error" onClick={() => setError("")}>×</button></div>}
			<div className="page-content">
				{page === "new-run" ? <RequirementForm onStart={start} busy={busy} /> : page === "url-demo" ? <URLShortener apiOnline={apiOnline} /> : page === "metrics" ? <MetricsView data={metrics} /> : page === "workflows" ? <><WorkflowList workflows={workflows} selected={workflow?.workflow_id} onSelect={id => { const selected = workflows.find(item => item.workflow_id === id); if (selected) setWorkflow(selected); }} />{workflow ? <WorkflowDetail workflow={workflow} onApprove={approve} onReject={reject} onClarify={clarify} busy={busy} /> : null}</> : <><Dashboard workflow={workflow} metrics={metrics} onApprove={approve} onReject={reject} busy={busy} /><ApprovalGate workflow={workflow} onApprove={approve} onReject={reject} busy={busy} /></>}
			</div>
		</main>
	</div>;
}