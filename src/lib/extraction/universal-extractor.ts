import { exec } from 'child_process';
import { promisify } from 'util';
import { writeFile, unlink } from 'fs/promises';
import path from 'path';
import os from 'os';

const execAsync = promisify(exec);

interface ExtractionResult {
    success: boolean;
    text?: string;
    error?: string;
    format?: string;
    is_scanned?: boolean;
}

/**
 * Extrait le texte de n'importe quel format de document
 * Utilise Python avec des bibliothèques open-source gratuites
 */
export async function extractTextFromDocument(
    buffer: Buffer,
    filename: string
): Promise<string> {
    const ext = path.extname(filename).toLowerCase();
    console.log(`[Universal Extractor] Processing ${ext} file...`);

    // Try Node.js native solutions first (no Python needed)
    if (ext === '.docx') {
        try {
            const mammoth = require('mammoth');
            const result = await mammoth.extractRawText({ buffer });
            console.log('[Universal Extractor] DOCX extracted with mammoth (Node.js)');
            return result.value;
        } catch (error) {
            console.error('[Universal Extractor] mammoth failed, trying Python:', error);
        }
    }

    if (ext === '.txt') {
        return buffer.toString('utf-8');
    }

    // For PDF, use dedicated extractor
    if (ext === '.pdf') {
        const { extractTextFromPdf } = require('./pdf-extractor');
        return await extractTextFromPdf(buffer);
    }

    // For other formats (DOC, ODT, RTF), use Python
    const tempDir = os.tmpdir();
    const tempFile = path.join(tempDir, `doc-${Date.now()}${ext}`);

    try {
        // Write buffer to temp file
        await writeFile(tempFile, buffer);
        console.log('[Universal Extractor] Temp file created:', tempFile);

        // Execute Python script - try multiple Python commands
        const scriptPath = path.join(process.cwd(), 'scripts', 'extract_document.py');

        // Try different Python commands (absolute path first, then common commands)
        const pythonCommands = [
            'C:\\Python314\\python.exe',  // Absolute path detected on this system
            process.env.PYTHON_PATH,      // Custom path from env if set
            'python',
            'python3',
            'py'
        ].filter(Boolean); // Remove undefined values

        let lastError: any;

        for (const pythonCmd of pythonCommands) {
            try {
                const command = `${pythonCmd} "${scriptPath}" "${tempFile}"`;
                console.log('[Universal Extractor] Trying:', command);

                const { stdout, stderr } = await execAsync(command, {
                    maxBuffer: 10 * 1024 * 1024,
                    timeout: 30000
                });

                if (stderr && !stderr.includes('UserWarning')) {
                    console.warn('[Universal Extractor] Python stderr:', stderr);
                }

                // Parse result
                const result: ExtractionResult = JSON.parse(stdout);
                console.log('[Universal Extractor] Result:', {
                    success: result.success,
                    format: result.format,
                    textLength: result.text?.length,
                    isScanned: result.is_scanned
                });

                // Cleanup temp file
                await unlink(tempFile).catch(e => console.warn('Failed to delete temp file:', e));

                if (result.success && result.text) {
                    return result.text;
                }

                // Handle specific errors
                if (result.is_scanned) {
                    throw new Error('PDF_SCANNED: Ce PDF est scanné. Veuillez utiliser l\'onglet "Scan Caméra" pour l\'OCR.');
                }

                throw new Error(result.error || 'Extraction failed');

            } catch (error: any) {
                lastError = error;
                if (error.code !== 'ENOENT') {
                    // If it's not a "command not found" error, throw it
                    throw error;
                }
                // Otherwise, try next Python command
                console.log(`[Universal Extractor] ${pythonCmd} not found, trying next...`);
            }
        }

        // If we get here, no Python command worked
        throw lastError;

    } catch (error: any) {
        // Cleanup on error
        await unlink(tempFile).catch(() => { });

        console.error('[Universal Extractor] Extraction failed:', error);

        // If Python not available, provide clear error
        if (error.message?.includes('python') || error.code === 'ENOENT') {
            throw new Error(
                'Python n\'est pas installé sur ce serveur. ' +
                'Veuillez installer Python et les dépendances (voir docs/EXTRACTION_SETUP.md) ' +
                'ou utilisez le format DOCX qui fonctionne sans Python.'
            );
        }

        // If dependencies missing
        if (error.message?.includes('not installed')) {
            throw new Error(
                'Dépendances Python manquantes. ' +
                'Exécutez: pip install PyMuPDF python-docx docx2txt odfpy striprtf'
            );
        }

        throw error;
    }
}

// Export specific extractors for backward compatibility
export async function extractTextFromPdf(buffer: Buffer): Promise<string> {
    return extractTextFromDocument(buffer, 'document.pdf');
}

export async function extractTextFromDocx(buffer: Buffer): Promise<string> {
    return extractTextFromDocument(buffer, 'document.docx');
}
