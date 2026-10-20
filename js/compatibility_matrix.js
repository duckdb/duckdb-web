// Probes the community extensions repository and fills in the Compatibility Matrix with check / x icons
(function () {
	const extensionName = document.currentScript && document.currentScript.dataset.extensionName;
	if (!extensionName) return;

	const upcomingVersions = ['2.0.0'];
	const platforms = {
		'linux amd64': 'linux_amd64',
		'linux arm64': 'linux_arm64',
		'macos amd64': 'osx_amd64',
		'macos arm64': 'osx_arm64',
		'windows amd64': 'windows_amd64',
		'windows arm64': 'windows_arm64',
	};

	function findMatrix() {
		const heading = document.getElementById('compatibility-matrix');
		if (!heading) return null;
		let el = heading.nextElementSibling;
		while (el && !/^H[1-6]$/.test(el.tagName)) {
			const table = el.tagName === 'TABLE' ? el : el.querySelector('table');
			if (table) return table;
			el = el.nextElementSibling;
		}
		return null;
	}

	async function isAvailable(url) {
		try {
			const response = await fetch(url, { method: 'HEAD' });
			return response.ok;
		} catch (e) {
			return false;
		}
	}

	// same markup as _plugins/emoji_replacer.rb
	function setIcon(cell, icon) {
		cell.innerHTML = `<svg class="icon ${icon}"><use xlink:href="#${icon}"></use></svg>`;
	}

	function setPending(cell) {
		cell.innerHTML = '<span style="color: var(--main-text-tertiary-color, #B2B2B2);">?</span>';
	}

	document.addEventListener('DOMContentLoaded', function () {
		const table = findMatrix();
		if (!table) return;

		const versions = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());

		table.querySelectorAll('tbody tr').forEach(row => {
			const cells = row.querySelectorAll('td');
			const platform = platforms[cells[0].textContent.trim().toLowerCase().replace(/\s+/g, ' ')];
			if (!platform) return;

			for (let i = 1; i < cells.length; i++) {
				const version = versions[i];
				const cell = cells[i];
				if (!version) continue;
				const content = cell.textContent.trim();
				if (content === '-') {
					setIcon(cell, 'x');
					continue;
				}
				// grey out the placeholder while the probe is pending
				if (content === '?') setPending(cell);
				const url = `https://community-extensions.duckdb.org/v${version}/${platform}/${extensionName}.duckdb_extension.gz`;
				// for upcoming versions, a missing binary may still arrive, so keep the grey question mark
				const unavailableIcon = upcomingVersions.includes(version) ? null : 'x';
				isAvailable(url).then(available => {
					if (available) setIcon(cell, 'check');
					else if (unavailableIcon) setIcon(cell, unavailableIcon);
					else setPending(cell);
				});
			}
		});
	});
})();
