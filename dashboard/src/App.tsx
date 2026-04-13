import { useState, useEffect, useRef } from 'react';
import { Folder, FileText, Share2, Link as LinkIcon, Download, Menu, FileBox } from 'lucide-react';
import mermaid from 'mermaid';

mermaid.initialize({ startOnLoad: false, theme: 'dark' });

export default function App() {
  const [tree, setTree] = useState<any>(null);
  const [selectedFile, setSelectedFile] = useState<any>(null);
  const [fileContent, setFileContent] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Fetch file tree on mount
  useEffect(() => {
    fetch('/api/projects')
      .then(r => r.json())
      .then(data => setTree(data))
      .catch(e => console.error("Could not fetch projects", e));
  }, []);

  // Fetch file content when selection changes
  useEffect(() => {
    if (!selectedFile || selectedFile.type !== 'file') return;
    setFileContent("Loading...");
    fetch(`/api/file?path=${encodeURIComponent(selectedFile.path)}`)
      .then(r => r.text())
      .then(text => setFileContent(text))
      .catch(e => setFileContent("Error loading file: " + e.message));
  }, [selectedFile]);

  return (
    <div className="flex h-screen w-full bg-slate-950 text-slate-300 font-sans overflow-hidden">
      {/* Sidebar */}
      <div className={`transition-all duration-300 border-r border-slate-800 bg-slate-900/50 backdrop-blur-md flex flex-col ${sidebarOpen ? 'w-80' : 'w-0 opacity-0 overflow-hidden'}`}>
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 font-semibold text-white">
            <Share2 className="w-5 h-5 text-blue-400" />
            The-Visualizer
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
          {tree ? <FileTree node={tree} onSelect={setSelectedFile} selectedPath={selectedFile?.path} /> : <div className="text-sm text-slate-500 animate-pulse">Scanning workspace...</div>}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        <header className="h-14 border-b border-slate-800 bg-slate-900/30 flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-1.5 hover:bg-slate-800 rounded-md text-slate-400 hover:text-white transition-colors">
              <Menu className="w-5 h-5" />
            </button>
            <div className="text-sm font-medium text-slate-200">
              {selectedFile ? selectedFile.name : 'Select a file to view'}
            </div>
          </div>
          
          {selectedFile && (
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-white rounded-md transition-colors border border-slate-700 shadow-sm"
                onClick={() => {
                  /* Optional: direct ide link logic */
                  navigator.clipboard.writeText(`vscode://file/${selectedFile.path}`);
                  alert('Copied absolute path/URI (simulated)');
                }}>
                <LinkIcon className="w-3.5 h-3.5 text-blue-400" />
                Copy IDE Link
              </button>
            </div>
          )}
        </header>

        <main className="flex-1 overflow-hidden bg-slate-950 p-6 relative flex flex-col">
          {selectedFile && fileContent ? (
             <FileViewer file={selectedFile} content={fileContent} />
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-slate-500 space-y-4">
              <FileBox className="w-16 h-16 opacity-20" />
              <p>Select a generated visualization from the sidebar to begin.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

// ---------------------------------------------------------
// Components
// ---------------------------------------------------------

function FileTree({ node, onSelect, selectedPath, depth = 0 }: { node: any, onSelect: (node: any) => void, selectedPath?: string, depth?: number }) {
  const [isOpen, setIsOpen] = useState(depth === 0);
  const isFile = node.type === 'file';
  const isSelected = selectedPath === node.path;

  if (isFile) {
    return (
      <div 
        className={`flex items-center gap-2 py-1.5 px-2 rounded-md cursor-pointer text-sm transition-colors ${isSelected ? 'bg-blue-500/20 text-blue-300' : 'hover:bg-slate-800/80 text-slate-400 hover:text-slate-200'}`}
        style={{ paddingLeft: `${depth * 1 + 0.5}rem` }}
        onClick={() => onSelect(node)}
      >
        <FileText className="w-4 h-4 opacity-70" />
        <span className="truncate">{node.name}</span>
      </div>
    );
  }

  return (
    <div className="mb-1">
      <div 
        className="flex items-center gap-2 py-1.5 px-2 hover:bg-slate-800/50 rounded-md cursor-pointer text-sm font-medium text-slate-300"
        style={{ paddingLeft: `${depth * 1 + 0.5}rem` }}
        onClick={() => setIsOpen(!isOpen)}
      >
        <Folder className={`w-4 h-4 ${isOpen ? 'text-blue-400' : 'text-slate-500'}`} />
        {node.name}
      </div>
      {isOpen && node.children && (
        <div className="mt-1">
          {node.children.map((child: any, idx: number) => (
            <FileTree key={idx} node={child} onSelect={onSelect} selectedPath={selectedPath} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

function FileViewer({ file, content }: { file: any, content: string }) {
  const isMarkdown = file.name.endsWith('.md');
  const isDot = file.name.endsWith('.dot');
  const isJson = file.name.endsWith('.json');
  
  if (content === "Loading...") {
    return <div className="text-center animate-pulse text-slate-400 pt-20">Loading render engine...</div>;
  }

  return (
    <div className="w-full h-full relative group">
      {/* Raw View Toggle / Download (Simplified view) */}
      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-10 flex gap-2">
        <button 
          className="bg-slate-800/90 text-slate-300 p-2 rounded hover:bg-slate-700 hover:text-white shadow-lg backdrop-blur"
          title="Download Raw File"
          onClick={() => {
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = file.name;
            a.click();
            URL.revokeObjectURL(url);
          }}
        >
          <Download className="w-4 h-4" />
        </button>
      </div>

      <div className="w-full h-full rounded-xl bg-slate-900 border border-slate-800 overflow-hidden shadow-2xl relative">
        {isMarkdown ? (
          <MermaidRenderer content={content} />
        ) : isDot ? (
          <GraphvizRenderer content={content} />
        ) : isJson ? (
          <pre className="p-6 text-xs text-green-400 font-mono overflow-auto h-full w-full">{content}</pre>
        ) : (
          <pre className="p-6 text-sm text-slate-300 font-mono overflow-auto h-full w-full break-all whitespace-pre-wrap">{content}</pre>
        )}
      </div>
    </div>
  );
}

function MermaidRenderer({ content }: { content: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    
    // Extract mermaid block from markdown accommodating Windows CRLF
    const mermaidRegex = /```mermaid[\r\n]+([\s\S]*?)```/;
    const match = content.match(mermaidRegex);
    const code = match ? match[1] : content; // Default to full content if no ticks found

    if (!code.trim()) {
      setError("No mermaid code found in this file.");
      return;
    }

    const renderGraph = async () => {
      try {
        setError(null);
        containerRef.current!.innerHTML = '';
        const id = `mermaid-${Date.now()}`;
        const { svg } = await mermaid.render(id, code);
        if (containerRef.current) {
          containerRef.current.innerHTML = svg;
          // Apply some flex centering to the SVG
          const svgEl = containerRef.current.querySelector('svg');
          if (svgEl) {
             svgEl.style.maxWidth = '100%';
             svgEl.style.height = 'auto';
             svgEl.style.margin = 'auto'; 
             svgEl.style.display = 'block';
          }
        }
      } catch (err: any) {
        setError(err.message || 'Error rendering Mermaid diagram');
        console.error(err);
      }
    };

    renderGraph();
  }, [content]);

  if (error) {
    return (
      <div className="p-6 text-red-400 h-full w-full overflow-auto font-mono text-sm break-all">
        <h3 className="text-red-500 font-bold mb-2">Render Error</h3>
        <pre>{error}</pre>
        <h3 className="text-slate-400 font-bold mt-4 mb-2">Raw File:</h3>
        <pre className="text-slate-500">{content}</pre>
      </div>
    );
  }

  return (
    <div className="w-full h-full flex items-center justify-center p-8 overflow-auto bg-slate-900/50">
       <div ref={containerRef} className="w-full max-w-5xl transition-all duration-500 ease-in-out" />
    </div>
  );
}

import { instance } from "@viz-js/viz";

function GraphvizRenderer({ content }: { content: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current || !content) return;

    let isMounted = true;
    
    instance().then(viz => {
      if (!isMounted) return;
      try {
        setError(null);
        containerRef.current!.innerHTML = "";
        const svgElement = viz.renderSVGElement(content);
        
        // Make the svg responsive
        svgElement.style.maxWidth = '100%';
        svgElement.style.height = 'auto';
        
        containerRef.current!.appendChild(svgElement);
      } catch (err: any) {
        setError(err.message || 'Error rendering Graphviz');
      }
    }).catch(err => {
      if (isMounted) setError(err.message || 'Failed to load viz.js instance');
    });

    return () => { isMounted = false; };
  }, [content]);

  if (error) {
    return (
      <div className="p-6 text-red-400 h-full w-full overflow-auto font-mono text-sm break-all">
        <h3 className="text-red-500 font-bold mb-2">Graphviz Error</h3>
        <pre>{error}</pre>
        <h3 className="text-slate-400 font-bold mt-4 mb-2">Raw File:</h3>
        <pre className="text-slate-500">{content}</pre>
      </div>
    );
  }

  return (
    <div className="w-full h-full overflow-hidden flex items-center justify-center bg-white rounded-xl">
      {/* We use bg-white because typical dot output depends on white bg for lines unless dark theme explicitly set in dot */}
      <div ref={containerRef} className="w-full h-full p-4 overflow-auto flex items-center justify-center" />
    </div>
  );
}
