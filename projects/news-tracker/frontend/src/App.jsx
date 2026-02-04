import React, { useEffect, useMemo, useState } from "react";
import ArticleDetailModal from "./components/ArticleDetailModal";
import {
  analyzeManual,
  createSource,
  createTopic,
  fetchArticles,
  fetchSources,
  fetchTopics,
  manualFetch,
  updateSource,
  updateTopic,
} from "./api.js";

const EMPTY_TOPIC = {
  name_zh: "",
  name_en: "",
  keywords: "",
  is_core: false,
  enabled: true,
};

const EMPTY_SOURCE = {
  name: "",
  url: "",
  lang: "en",
  priority: 0,
  topic_id: "",
  enabled: true,
};

export default function App() {
  const [view, setView] = useState("news");
  const [topics, setTopics] = useState([]);
  const [sources, setSources] = useState([]);
  const [articlesByTopic, setArticlesByTopic] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [topicForm, setTopicForm] = useState(EMPTY_TOPIC);
  const [sourceForm, setSourceForm] = useState(EMPTY_SOURCE);
  const [manualText, setManualText] = useState("");
  const [manualResult, setManualResult] = useState("");
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [activeTopicId, setActiveTopicId] = useState("all");

  const sortedTopics = useMemo(() => {
    return [...topics].sort((a, b) => {
      if (a.is_core && !b.is_core) return -1;
      if (!a.is_core && b.is_core) return 1;
      return a.name_zh.localeCompare(b.name_zh, "zh");
    });
  }, [topics]);

  // Load data on mount
  useEffect(() => {
    loadAll();
  }, []);

  async function loadAll() {
    setLoading(true);
    setError("");
    try {
      const topicList = await fetchTopics();
      setTopics(topicList);
      const sourceList = await fetchSources();
      setSources(sourceList);
      const nextArticles = {};
      for (const topic of topicList) {
        const items = await fetchArticles(topic.id, 3);
        nextArticles[topic.id] = items;
      }
      setArticlesByTopic(nextArticles);
    } catch (err) {
      setError(err.message || "加载失败");
    } finally {
      setLoading(false);
    }
  }

  async function handleManualFetch() {
    setLoading(true);
    setError("");
    try {
      await manualFetch();
      await loadAll();
    } catch (err) {
      setError(err.message || "刷新失败");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateTopic(e) {
    e.preventDefault();
    setError("");
    try {
      await createTopic({
        ...topicForm,
        is_core: Boolean(topicForm.is_core),
        enabled: Boolean(topicForm.enabled),
      });
      setTopicForm(EMPTY_TOPIC);
      await loadAll();
    } catch (err) {
      setError(err.message || "创建主题失败");
    }
  }

  async function handleToggleTopic(topic) {
    try {
      await updateTopic(topic.id, { enabled: !topic.enabled });
      await loadAll();
    } catch (err) {
      setError(err.message || "更新主题失败");
    }
  }

  async function handleCreateSource(e) {
    e.preventDefault();
    setError("");
    try {
      const payload = { ...sourceForm };
      if (!payload.topic_id) payload.topic_id = null;
      else payload.topic_id = Number(payload.topic_id);
      await createSource(payload);
      setSourceForm(EMPTY_SOURCE);
      await loadAll();
    } catch (err) {
      setError(err.message || "创建来源失败");
    }
  }

  async function handleToggleSource(source) {
    try {
      await updateSource(source.id, { enabled: !source.enabled });
      await loadAll();
    } catch (err) {
      setError(err.message || "更新来源失败");
    }
  }

  async function handleManualAnalyze() {
    setError("");
    setManualResult("");
    const titles = manualText.split("\n").map((line) => line.trim()).filter(Boolean);
    if (!titles.length) {
      setError("请输入至少一条标题");
      return;
    }
    try {
      const result = await analyzeManual(titles);
      setManualResult(result.response_text);
    } catch (err) {
      setError(err.message || "分析失败");
    }
  }



  return (
    <div className="page">
      <header className="topbar">
        <div>
          <h1>新闻追踪</h1>
          <span>最近3天 · 英文优先 / 中文同源优先</span>
        </div>
        <div className="topbar-actions">
          <button onClick={() => setView("news")} className={view === "news" ? "active" : ""}>
            新闻
          </button>
          <button onClick={() => setView("analysis")} className={view === "analysis" ? "active" : ""}>
            分析
          </button>
          <button onClick={() => setView("manage")} className={view === "manage" ? "active" : ""}>
            管理
          </button>
          <button className="primary" onClick={handleManualFetch}>
            手动刷新
          </button>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}
      {loading && <div className="loading">加载中...</div>}

      {view === "news" && (
        <div className="content">
          <div className="topic-tabs">
            <button
              className={activeTopicId === "all" ? "tab active" : "tab"}
              onClick={() => setActiveTopicId("all")}
            >
              全部
            </button>
            {sortedTopics.map(t => (
              <button
                key={t.id}
                className={activeTopicId === t.id ? "tab active" : "tab"}
                onClick={() => setActiveTopicId(t.id)}
              >
                {t.name_zh}
              </button>
            ))}
          </div>

          {sortedTopics
            .filter(topic => activeTopicId === "all" || topic.id === activeTopicId)
            .map((topic) => (
              <section key={topic.id} className="topic-section">
                <div className="topic-header">
                  <h2>{topic.name_zh}</h2>
                  {topic.is_core && <span className="tag">核心</span>}
                </div>
                <div className="article-grid">
                  {(articlesByTopic[topic.id] || []).map((article) => (
                    <div
                      key={article.id}
                      className="card"
                      onClick={() => setSelectedArticle(article)}
                      style={{ cursor: "pointer" }}
                    >
                      <div className="card-title">{article.title_zh}</div>
                      <div className="card-meta">
                        <span>{article.source_name}</span>
                        <span>{article.published_at ? new Date(article.published_at).toLocaleString() : ""}</span>
                      </div>
                      <div className="card-tags">
                        <span className={article.is_primary_lang ? "tag" : "tag muted"}>
                          {article.is_primary_lang ? "主" : "辅"}
                        </span>
                        <span className="tag">{article.relevance_label}</span>
                        <span className="tag">{article.finance_score.toFixed(2)}</span>
                      </div>
                      {article.summary_zh && <div className="card-summary">{article.summary_zh}</div>}
                      <div className="card-hint">
                        点击查看 AI 摘要及原文...
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            ))}
          <ArticleDetailModal
            article={selectedArticle}
            onClose={() => setSelectedArticle(null)}
          />
        </div>
      )}

      {view === "analysis" && (
        <div className="content">
          <section className="panel wide">
            <h2>手动分析标题</h2>
            <p>每行一个标题，提交后生成经济意义简析。</p>
            <textarea
              rows="6"
              placeholder="输入标题，一行一个"
              value={manualText}
              onChange={(e) => setManualText(e.target.value)}
            />
            <button className="primary" onClick={handleManualAnalyze}>
              开始分析
            </button>
            {manualResult && <pre className="result">{manualResult}</pre>}
          </section>
        </div>
      )}

      {view === "manage" && (
        <div className="content grid-2">
          <section className="panel">
            <h2>主题管理</h2>
            <form onSubmit={handleCreateTopic} className="form">
              <input
                placeholder="中文名称"
                value={topicForm.name_zh}
                onChange={(e) => setTopicForm({ ...topicForm, name_zh: e.target.value })}
              />
              <input
                placeholder="英文名称"
                value={topicForm.name_en}
                onChange={(e) => setTopicForm({ ...topicForm, name_en: e.target.value })}
              />
              <input
                placeholder="关键词 (逗号分隔)"
                value={topicForm.keywords}
                onChange={(e) => setTopicForm({ ...topicForm, keywords: e.target.value })}
              />
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={topicForm.is_core}
                  onChange={(e) => setTopicForm({ ...topicForm, is_core: e.target.checked })}
                />
                设为核心主题
              </label>
              <button type="submit">新增主题</button>
            </form>

            <div className="list">
              {sortedTopics.map((topic) => (
                <div key={topic.id} className="list-item">
                  <div>
                    <strong>{topic.name_zh}</strong>
                    <span>{topic.keywords}</span>
                  </div>
                  <button onClick={() => handleToggleTopic(topic)}>
                    {topic.enabled ? "禁用" : "启用"}
                  </button>
                </div>
              ))}
            </div>
          </section>

          <section className="panel">
            <h2>来源管理</h2>
            <form onSubmit={handleCreateSource} className="form">
              <input
                placeholder="来源名称"
                value={sourceForm.name}
                onChange={(e) => setSourceForm({ ...sourceForm, name: e.target.value })}
              />
              <input
                placeholder="RSS 地址"
                value={sourceForm.url}
                onChange={(e) => setSourceForm({ ...sourceForm, url: e.target.value })}
              />
              <div className="row">
                <select
                  value={sourceForm.lang}
                  onChange={(e) => setSourceForm({ ...sourceForm, lang: e.target.value })}
                >
                  <option value="en">英文</option>
                  <option value="zh">中文</option>
                </select>
                <input
                  type="number"
                  placeholder="优先级"
                  value={sourceForm.priority}
                  onChange={(e) => setSourceForm({ ...sourceForm, priority: Number(e.target.value) })}
                />
              </div>
              <select
                value={sourceForm.topic_id}
                onChange={(e) => setSourceForm({ ...sourceForm, topic_id: e.target.value })}
              >
                <option value="">全部主题</option>
                {sortedTopics.map((topic) => (
                  <option key={topic.id} value={topic.id}>
                    {topic.name_zh}
                  </option>
                ))}
              </select>
              <button type="submit">新增来源</button>
            </form>

            <div className="list">
              {sources.map((source) => (
                <div key={source.id} className="list-item">
                  <div>
                    <strong>{source.name}</strong>
                    <span>{source.url}</span>
                  </div>
                  <button onClick={() => handleToggleSource(source)}>
                    {source.enabled ? "禁用" : "启用"}
                  </button>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
      <footer style={{
        textAlign: 'center',
        padding: '20px',
        color: '#666',
        fontSize: '0.8rem',
        marginTop: 'auto',
        borderTop: '1px solid rgba(255,255,255,0.05)'
      }}>
        已连接服务器: {import.meta.env.VITE_API_BASE || "http://localhost:8000"}
        {import.meta.env.VITE_API_BASE?.includes("192.168") ? " (远程)" : " (本地)"}
      </footer>
    </div>
  );
}
